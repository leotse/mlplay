"""
data loader that provides function to load data with different features (X)
and output (Y)
"""

from data.db import DB


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
        rows = [row for row in self.db.select(ticker)]

        # calc the adjusted changes
        adj_changes = [day1['adj_close'] - day0['adj_close']
                       for [day0, day1] in zip(rows[:-1], rows[1:])]

        # build data matrix X
        X_rows = zip(*[rows[i:] for i in xrange(n)])
        X = [[day[field] for day in days for field in ['adj_close', 'volume']]
             for days in X_rows]

        # remove latest day from training data X
        # remove the first n days of data from label data y
        return X[:-1], adj_changes[n - 1:]

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

        # build output vector y
        # which is the change of the y field
        # y = []
        # for item in zip(y_values, y_values[1:]):
        #     y.append(item[1] - item[0])

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
