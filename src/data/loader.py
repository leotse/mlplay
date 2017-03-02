"""
data loader that provides function to load data with different features (X)
and output (y)
"""

import os
import pandas as pd

from data.db import DB

def load(ticker):
    """Load price data for ticker"""
    rel_path = 'tmp/{0}.csv'.format(ticker.lower())
    abs_path = os.path.realpath(rel_path)
    df = pd.read_csv(abs_path, index_col=1, parse_dates=True)

    # add change % series
    df['change'] = (df['close'] - df['open']) / df['open'] * 100.0

    # ignore rows with missing data
    return df

def load_history(ticker, field, n):
    """ load n days field history"""
    df = load(ticker)

    # build n-days history for the given field
    def reducer(series, i):
        """reducer to create the data series dict"""
        series['{0}-{1}'.format(field, i)] = df[field].shift(i)
        return series
    series_dict = reduce(reducer, xrange(0, n), {})

    # create DataFrame and drop NaNs
    return pd.DataFrame(data=series_dict)

class Loader(object):
    """Loader contains functions to load and format data for model training"""

    def __init__(self, dbpath):
        self.db = DB(dbpath)
        self.db.__enter__()

    def __del__(self):
        self.db.__exit__(None, None, None)

    def load_change_history(self, ticker, n):
        """
        load price change history for the given ticker and number of days (n)
        """

        # get price data for the ticker from db
        rows = [row for row in self.db.select_change(ticker, fields=[
            'adj_open',
            'adj_close',
            'adj_volume'
        ])]

        # select only the desired fields from the db rows
        X = [(row['adj_open'],
              row['adj_close'],
              row['adj_volume'],
              row['adj_change']) for row in rows]

        # combine n days of history into one row
        X = zip(*[X[i:] for i in xrange(n)])

        # then flatten eachrow
        def flatten(row):
            """flattens a row"""
            return reduce(lambda t1, t2: t1 + t2, row)
        X = [flatten(row) for row in X]

        # and label vector y that lines up with X
        y = [row['adj_change'] for row in rows]

        # remove latest day from training data X
        # remove the first n days of data from label data y
        return X[:-1], y[n:]

    def load_price_history(self, ticker, n, x_fields, y_field):
        """
        load price history for the given ticker, days (n),
        data fields (X) and label field (y)
        """

        # get all price data for ticker from db
        prices = self.buffer(self.db.select(ticker))

        # select only the required fields for X and y
        X_values = [self.select_fields(price, x_fields) for price in prices]
        y_values = [price[y_field] for price in prices]

        # build feature vector X
        # this vector starts at index 5 of the original data
        X = []
        n_columns = [X_values[i:] for i in xrange(n)]
        for item in zip(*n_columns):
            row = [vals[i] for
                   vals in item for
                   i in range(len(x_fields))]
            X.append(row)

        # removing the final row since the feature matrix
        # should not have knowledge of the latest price
        X = X[:-1]

        # line up with the feature matrix X
        return X, y_values[n:]

    @staticmethod
    def select_fields(price, fields):
        """get given fields from price object and
        return as array"""
        return [price[field] for field in fields]

    @staticmethod
    def buffer(cursor):
        """buffer all items from cursor in memory"""
        def reducer(buffered, item):
            """appends given item to list"""
            buffered.append(item)
            return buffered
        return reduce(reducer, cursor, [])
