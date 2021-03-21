from dbaccess import DBAcess
import sys

from bs4 import BeautifulSoup
from const import CONST
import requests
from datetime import datetime
import re
from contextlib import closing
import csv
import codecs
from dateutil.parser import parse
import time

class TiblioScraper:

    def __init__(self):
        self.session = self.__signon()
        self.last_updated_naked_shorts = datetime(2001,1,1)
        self.last_updated_long_calls_puts = {"CALLS": datetime(2001,1,1), "PUTS": datetime(2001,1,1)}
        self.last_updated_short_credit_spreads = datetime(2001,1,1)
        self.db = DBAcess()

    def __signon(self):
        s = requests.session()
        resp = s.get(CONST.URL_SIGNIN)
        csrftoken = resp.cookies['csrftoken']

        cred = {
                "username": CONST.TIBLIO_USER,
                "password": CONST.TIBLIO_PASSWORD,
                "csrfmiddlewaretoken": csrftoken
                }

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        headers['content-type'] = 'application/x-www-form-urlencoded'
        req = s.post(CONST.URL_SIGNIN, data=cred, headers=headers)

        if req.status_code != 200:
            raise Exception(f"Unable to LOGON: {cred}")
        else:
            return s

    def _check_updated_naked_shorts(self):
        updated_time = self._get_updated_date(CONST.URL_NAKED_SHORTS)

        if updated_time > self.last_updated_naked_shorts:

            self.last_updated_naked_shorts = updated_time
            return True
        else:
            return False

    def _get_updated_date(self, url):
        resp = self.session.get(url, headers=dict(Referer=CONST.URL_SIGNIN))
        if resp.status_code != 200:
            raise Exception(f"Unable to check the {url}")

        soup = BeautifulSoup(resp.text, "html.parser")
        updated_time = datetime.now()

        for tag in soup.find_all("div", {"class": "card-actions"}):
            updated = tag.parent.findNext('p')
            updated = updated.contents[0]
            updated_time = re.findall(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}, [\d]{1,2}:[\d]{1,2} [ap].m.", updated)[0]
            updated_time = parse(updated_time)
            return updated_time

        return datetime(1999,1,1)


    def _check_updated_short_spreads(self):
        updated_time = self._get_updated_date(CONST.URL_SHORT_CREDIT_SPREADS)

        if updated_time > self.last_updated_short_credit_spreads:

            self.last_updated_short_credit_spreads = updated_time
            return True
        else:
            return False

    def load_short_spreads(self):
        if self._check_updated_short_spreads():
            print(f"Processing at {self.last_updated_short_credit_spreads}")
            
            try:
                with closing(self.session.get(CONST.URL_DOWNLOAD_CREDIT_LIST,
                    headers=dict(Referer=CONST.URL_SHORT_CREDIT_SPREADS), stream=True)) as r:
                    reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',', quotechar='"')
                    next(reader) # skip the header

                    self.db.insert_credit_spreads(reader)

            except Exception as e:
                print (e)
        else:
            print(f"Skipping stale data at {self.last_updated_naked_shorts}")



    def load_naked_shorts(self):
        # The short put screener is non-directional in nature; it finds the most out of the money with the best credit (expensive). 
        if self._check_updated_naked_shorts():
            print(f"Processing at {self.last_updated_naked_shorts}")
            
            try:
                with closing(self.session.get(CONST.URL_DOWNLOAD_LIST_SINGLES, 
                    headers=dict(Referer=CONST.URL_NAKED_SHORTS), stream=True)) as r:
                    reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',', quotechar='"')
                    next(reader) # skip the header

                    self.db.insert_naked_shorts(reader)

            except Exception as e:
                print (e)
        else:
            print(f"Skipping stale data at {self.last_updated_naked_shorts}")

    def _load_long_calls_puts(self, res_text, txn):
        soup = BeautifulSoup(res_text, "html.parser")
        updated_time = datetime.now()
        updated_str = ""

        for tag in soup.find_all("div", {"class": "card-header"}):
            updated = tag.findNext('p')
            updated = updated.contents[0]
            updated_str = re.findall(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}, [\d]{1,2}:[\d]{1,2} [ap].m.", updated)[0]
            updated_time = parse(updated_str)

        if updated_time > self.last_updated_long_calls_puts[txn]:
            print(f"Processing at {self.last_updated_long_calls_puts[txn]}")
            self.last_updated_long_calls_puts[txn] = updated_time

            reader = []
            for row in soup.select('tbody tr'):
                row_text = [x.text for x in row.find_all('td')]
                row_text.append(txn)
                row_text.append(updated_time)
                print(row_text)
                reader.append(row_text)

            self.db.insert_long_calls_puts(reader)
        else:
            print(f"Skipping stale data at {self.last_updated_long_calls_puts[txn]}")


#Case where I found sell puts and buy puts.

#On the put seller side this would cause me to go further out of the money or I may avoid the trade even though premiums are high.
#This is not a signal for a straddle because the short put screener is non directional. There is not a directional bias there.
#On the buy side, the put showing up on the short screener confirms that the puts are expensive, 
#but I already know that because the nature of the long put screener is that puts are trading on the ask, iv is going up, price is going up

    def load_long_calls(self):
        resp = self.session.get(CONST.URL_LONG_CALLS, headers=dict(Referer=CONST.URL_SIGNIN))
        if resp.status_code != 200:
            raise Exception(f"Unable to check the {CONST.URL_NAKED_SHORTS}")
        self._load_long_calls_puts(resp.text, 'CALLS')

    def load_long_puts(self):
        # Most out of the money with expensive premium
        #
        # The long put screener finds stocks that are trading with high iv with a lot of puts being purchased near the ask.

        resp = self.session.get(CONST.URL_LONG_PUTS, headers=dict(Referer=CONST.URL_SIGNIN))
        if resp.status_code != 200:
            raise Exception(f"Unable to check the {CONST.URL_NAKED_SHORTS}")
        self._load_long_calls_puts(resp.text, 'PUTS')

    def load_earnings_report(self):
#        resp = self.session.get(CONST.URL_)
        # TODO: work on earnings report.  Should be very similar to long_calls_puts
        pass

    
def run(argv) -> None:
    scraper = TiblioScraper()
    while True:
        scraper.load_short_spreads()
        scraper.load_naked_shorts()
        scraper.load_long_calls()
        scraper.load_long_puts()
        # TODO: put unittest automatically regression test upon save
        # scraper.load_earnings_report()
        # TODO: load market open schedule from somewhere and adjust the loading frequency.
        print("Sleeping for two minutes")
        time.sleep(120)

    
if __name__ == '__main__':
    run(sys.argv)
