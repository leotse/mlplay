"""
warm up #2 - simple linear regression on price change
"""

from data.loader import Loader

# args
TICKER = 'TSLA'
DAYS = 5

# load price change data
loader = Loader('tmp/prices_all.db')
X, y = loader.load_change_history(TICKER, DAYS)

print '{0} {1}'.format(X[0], y[0])
print '{0} {1}'.format(X[1], y[1])
print '{0} {1}'.format(X[2], y[2])
print '{0} {1}'.format(X[3], y[3])
print '{0} {1}'.format(X[4], y[4])

print '====='

print '{0} {1}'.format(X[-5], y[-5])
print '{0} {1}'.format(X[-4], y[-4])
print '{0} {1}'.format(X[-3], y[-3])
print '{0} {1}'.format(X[-2], y[-2])
print '{0} {1}'.format(X[-1], y[-1])
