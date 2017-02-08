# load data for the given ticker and date range

import sys

from data.data_loader import Loader
from common.utils import log

dbpath = sys.argv[1]

log('using db {0}'.format(dbpath))

loader = Loader(dbpath)
data = loader.combine_n_days('TSLA', n=5)

for i in xrange(-5, 0):
    print '{0} {1}'.format(data['X'][i], data['y'][i])
