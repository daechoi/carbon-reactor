from contextlib import closing
from const import CONST
import psycopg2

class DBAcess:
    def __init__(self):
        self.conn_str = f"host='{CONST.DB_HOST}' dbname='{CONST.DB_NAME}' user='{CONST.DB_USER}' password='{CONST.DB_PASS}' port='{CONST.DB_PORT}'"

    def _insert_cmd(self, sqlcmd, reader):
        sqlcmd = sqlcmd+ " ON CONFLICT DO NOTHING" # dedupe
        with closing(psycopg2.connect(self.conn_str)) as conn, conn.cursor() as cur:
            rec_cnt = 0
            for row in reader:
                rec_cnt = rec_cnt+1
                print (f"{rec_cnt}: {row}")
                cur.execute(sqlcmd, row)
                conn.commit()

    def insert_long_calls_puts(self, reader):
        sql_insert = """INSERT INTO public.staging_long_calls_puts
        (symbol, company_name, avg_daily_call_vol, current_call_open_int, txn, site_updated)
        VALUES(%s, %s, %s, %s, %s, %s) """
        self._insert_cmd(sql_insert, reader)

    def insert_naked_shorts(self,reader):
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
        values(%s, %s, %s, %s, %s, %s, cast(right(replace(%s,',',''),-1) as float4), cast(right(replace(%s,',',''),-1) as float4), %s, %s) """
        self._insert_cmd(sql_insert, reader)

    def insert_credit_spreads(self,reader):
        sql_insert = """INSERT INTO public.staging_credit_spreads
            (txn, symbol, expiration, put_call, short_strike, long_strike, initial_stock_price, pop, credit, maxloss, created, link)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s,  cast(right(replace(%s,',',''),-1) as float4), cast(right(replace(%s,',',''),-1) as float4), %s, %s) """

        self._insert_cmd(sql_insert, reader)


