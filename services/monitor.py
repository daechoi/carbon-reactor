import requests
from bs4 import BeautifulSoup
import time
from dateutil.parser import parse
import re
from datetime import datetime
from dotenv import load_dotenv
import os
from contextlib import closing
import csv
import codecs
import psycopg2 

from pathlib import Path
env_path = Path('.') / '.env.production'
load_dotenv(dotenv_path=env_path)

s = requests.session()
res = s.get("https://tiblio.com/signin")
if 'csrftoken' in res.cookies:
   csrftoken = res.cookies['csrftoken']
else:
   csrftoken = res.cookies['csrf']

payload = {
       "username": os.getenv("username"),
       "password": os.getenv("password"),
       "csrfmiddlewaretoken": csrftoken
       }

url = "https://tiblio.com/options-research/naked-puts"

naked_list = "https://tiblio.com/download-list-singles"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# download the homepage

headers['content-type'] = 'application/x-www-form-urlencoded'
req = s.post("https://tiblio.com/signin", data=payload, headers=headers)
# parse the downloaded homepage and grab all text, then,

last_updated = datetime(2014,5,1)

while True:
    response = s.get(url, headers=dict(Referer="https://tiblio.com/siginin"))
    soup = BeautifulSoup(response.text, "html.parser")
    
    updated_time = datetime.now()
    print(f"Checking now {updated_time}")

    for tag in soup.find_all("div", {"class": "card-actions"}):
        try:
            updated = tag.parent.findNext('p')
            updated_time = updated.contents[0]

            updated_time = re.findall(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}, [\d]{1,2}:[\d]{1,2} [ap].m.", updated_time)[0]

            updated_time = parse(updated_time)

        except Exception as e:
            print (e)

    if updated_time > last_updated:
        last_updated = updated_time
        print(f"processing with updated_time: {updated_time}")
       
        try:
            with closing(s.get(naked_list, headers=dict(Referer=url), stream=True)) as r:
                reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',', quotechar='"')
                next(reader) # skip the header
                dbname = os.getenv("POSTGRES_DB")
                user = os.getenv("POSTGRES_USER")
                password = os.getenv("POSTGRES_PASSWORD")
                conn_str = f"host='localhost' dbname='{dbname}' user='{user}' password='{password}' port='5433'"
                print(conn_str)
                sql_insert = """INSERT into public.staging_naked(
                    txn,
                    symbol,
                    expiration,
                    put_call,
                    strike,
                    pop,
                    credit,
                    maxloss,
                    created,
                    link
                )
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                with closing(psycopg2.connect(conn_str)) as conn, conn.cursor() as cur:
                    rec_cnt = 0
                    for row in reader:
                        rec_cnt = rec_cnt+1
                        print (f"{rec_cnt}: {row}")
                        cur.execute(sql_insert, row)
                        conn.commit()

                print("Finished reading.")
        except Exception as e:
            print (e)


        # create an email message with just a subject line,
        msg = 'Subject: This is Dae\'s script talking, Loading Tiblio!'
        # set the 'from' address,
        fromaddr = 'YOUR_EMAIL_ADDRESS'
        # set the 'to' addresses,
        toaddrs  = ['AN_EMAIL_ADDRESS','A_SECOND_EMAIL_ADDRESS', 'A_THIRD_EMAIL_ADDRESS']
        
        # setup the email server,
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # add my account login name and password,
        # server.login("YOUR_EMAIL_ADDRESS", "YOUR_PASSWORD")
        
        # Print the email's contents
        print('From: ' + fromaddr)
        print('To: ' + str(toaddrs))
        print('Message: ' + msg)
        
        # send the email
        # server.sendmail(fromaddr, toaddrs, msg)
        # disconnect from the server
        # server.quit()
        
    print("Sleeping for a minute")
    time.sleep(60)
 
