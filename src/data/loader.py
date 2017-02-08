# data loader that prices function to load data with different features (X) and output (Y)

from db import DB

FIELDS_ALL = ['adj_open', 'adj_high', 'adj_low', 'adj_close', 'adj_volume', 'split_ratio']

class Loader:

    def __init__(self, dbpath):
        self.db = DB(dbpath)
        self.db.__enter__()

    def __del__(self):
        self.db.__exit__(None, None, None)

    def combine_n_days(self, 
                        ticker,
                        n=5,
                        x_fields=['adj_open', 'adj_high', 'adj_low'],
                        y_field='adj_close'):

        prices_cursor = self.db.select(ticker)
        prices = self.buffer(prices_cursor)

        X_values = map(lambda price: 
            self.select_fields(price, x_fields), prices)
        y_values = map(lambda price: 
            price[y_field], prices)[n:]

        X_rows = []
        for item in zip(*(X_values[i:] for i in xrange(n))):
            row = [vals[i] for 
                   vals in item for 
                   i in range(len(x_fields))]
            X_rows.append(row)

        return { 'X': X_rows, 'y': y_values }
    
    def select_fields(self, price, fields):
        return [ price[field] for field in fields ]

    def buffer(self, cursor):
        def reducer(all, item):
            all.append(item)
            return all
        return reduce(reducer, cursor, [])