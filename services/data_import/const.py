from pathlib import Path
from dotenv import load_dotenv
import os


class Setting:

    def __init__(self):
        if os.getenv("environment") == "docker":
            env_path = Path("..") / '.env.docker'
        else:
            env_path = Path("..") / '.env.production'

        load_dotenv(dotenv_path=env_path)
        load_dotenv(dotenv_path=Path("..") / 'env.kafka')

        self.TIBLIO_USER = os.getenv("username")
        self.TIBLIO_PASSWORD = os.getenv("password")
        self.URL_SIGNIN = os.getenv("url_signin","") 
        self.URL_NAKED_SHORTS = os.getenv("url_naked_shorts","")
        self.URL_SHORT_CREDIT_SPREADS = os.getenv("url_short_credit_spreads","")
        self.URL_DOWNLOAD_CREDIT_LIST = os.getenv("url_download_credit_list","")
        self.URL_LONG_CALLS = os.getenv("url_long_calls","")
        self.URL_LONG_PUTS = os.getenv("url_long_puts","")
        self.URL_DOWNLOAD_LIST_SINGLES = os.getenv("url_download_list_singles","")
        self.DB_HOST = os.getenv("DB_HOST","")
        self.DB_USER = os.getenv("POSTGRES_USER","")
        self.DB_PASS = os.getenv("POSTGRES_PASSWORD","")
        self.DB_NAME = os.getenv("POSTGRES_DB","")
        self.DB_PORT = os.getenv("DB_PORT","")

        self.FINHUB_API = os.getenv("FINHUB_API","")
        self.URL_FINNHUB_WS_API = os.getenv("URL_FINNHUB_WS_API","")

        self.KAFKA_BROKER='localhost:9092'
        self.TOPIC_TRADES = os.getenv("TOPIC_TRADES")
        self.TOPIC_SHORT_PUTS = os.getenv("TOPIC_SHORT_PUTS")
        self.TOPIC_SHORT_CREDIT_SPREADS = os.getenv("TOPIC_SHORT_SHORT_CREDIT_SPREADS")
        self.TOPIC_LONG_CALLS_PUTS = os.getenv("TOPIC_LONG_CALLS_PUTS")
        self.TOPIC_EARNINGS_PLAYS = os.getenv("TOPIC_EARNINGS_PLAYS")

CONST = Setting()
