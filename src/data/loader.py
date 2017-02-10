# data loader that prices function to load data with different features
# (X) and output (Y)

from db import DB


class Loader:

    def __init__(self, dbpath):
        self.db = DB(dbpath)
        self.db.__enter__()

    def __del__(self):
        self.db.__exit__(None, None, None)

    def n_days_history(self,
                       ticker,
                       n=5,
                       x_fields=['adj_close'],
                       y_field='adj_close'):

        # get all price data for ticker from db
        prices_cursor = self.db.select(ticker)
        prices = self.buffer(prices_cursor)

        # select only the required fields for X and y
        X_values = map(lambda price:
                       self.select_fields(price, x_fields), prices)
        y_values = map(lambda price: price[y_field], prices)

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
        y = []
        for item in zip(y_values, y_values[1:]):
            y.append(item[1] - item[0])
        
        # line up with the feature matrix X
        y = y[n-1:]
        
        # return X and y
        return X, y

    def select_fields(self, price, fields):
        return [price[field] for field in fields]

    def buffer(self, cursor):
        def reducer(all, item):
            all.append(item)
            return all
        return reduce(reducer, cursor, [])
