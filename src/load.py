"""load data for the given ticker and date range"""

import sys

from data.loader import Loader
from common.utils import log

dbpath = sys.argv[1]

log('using db {0}'.format(dbpath))

loader = Loader(dbpath)
X, y = loader.load_price_history(ticker='TSLA', n=5,
                                 x_fields=['adj_volume', 'adj_close'],
                                 y_field='adj_close')

for i in xrange(0, 5):
    print '{0} {1}'.format(X[i], y[i])
