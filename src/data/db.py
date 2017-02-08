# sqlite3 db wrapper

import os
import sqlite3

import arrow

from common.utils import log

TABLE_PRICES = 'prices'


class DB:

    def __init__(self, path):
        self.dbpath = os.path.realpath(path)

    def __enter__(self):
        log('[db] connecting to {0}..'.format(self.dbpath))
        self.conn = sqlite3.connect(self.dbpath)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        log('[db] closing..')
        self.conn.commit()
        self.conn.close()

    def select(self,
               ticker,
               start_date=arrow.get(0).datetime,
               end_date=arrow.get().datetime):

        return self.cursor.execute(
            '''
            SELECT * FROM prices 
            WHERE ticker=?
            AND datetime>=?
            AND datetime<=?
            ORDER BY datetime ASC
            ''',
            (ticker, start_date, end_date)
        )

    def reset(self):
        log('[db] resetting prices db..')
        self.drop_table()
        self.ensure_table()
        self.ensure_indices()

    def drop_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS prices')

    def ensure_indices(self):
        self.cursor.execute(
            '''
            CREATE INDEX IF NOT EXISTS ticker_datetime
                ON prices (ticker, datetime)
            '''
        )

    def ensure_table(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS prices(
                id INTEGER PRIMARY KEY,
                datetime DATETIME,
                ticker TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                adj_open REAL,
                adj_high REAL,
                adj_low REAL,
                adj_close REAL,
                adj_volume REAL,
                split_ratio REAL,
                dividend REAL
            )
            '''
        )

    def insert_many(self, prices):
        rows = map(lambda price: [
            None,
            price['date'].datetime,
            price['ticker'],
            price['open'],
            price['high'],
            price['low'],
            price['close'],
            price['volume'],
            price['adj_open'],
            price['adj_high'],
            price['adj_low'],
            price['adj_close'],
            price['adj_volume'],
            price['split_ratio'],
            price['dividend']
        ], prices)
        self.cursor.executemany(
            'INSERT INTO prices values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            rows
        )
        self.conn.commit()
