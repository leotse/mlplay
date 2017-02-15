"""
warm up - simple linear regression on price data to predict price

findings: linear regression even with polynomial features performs quite
poorly in general; which is expected as it is hard to imagine linear
models can successfully model market dynamics; model was able to find
signal in some stocks but requires special sets of hyper parameters

insights: in the final system it's very likely that individual stocks
will need their own set of hyper parameters to work well
"""

import random

from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

import scoring
from data.loader import Loader

# stock to train
TICKER = 'FB'

# hyper parameters
N_DAYS = 50
DEGREE = 2
ALPHA = 0.1
Y_FIELD = 'adj_close'
X_FIELDS = ['adj_open', 'adj_close', 'adj_volume']

# load price data
loader = Loader('tmp/prices_all.db')
X_orig, y_orig = loader.load_price_history(TICKER, n=N_DAYS,
                                           x_fields=X_FIELDS,
                                           y_field=Y_FIELD)
X_orig_last_price = [x[-2] for x in X_orig]

# add polynomial features
poly = PolynomialFeatures(degree=DEGREE)
poly.fit(X_orig)
X = poly.transform(X_orig)
y = y_orig

# shuffle X and y
rand_indices = random.sample(list(range(len(X))), len(X))
X = [X[i] for i in rand_indices]
y = [y[i] for i in rand_indices]
X_last_price = [X_orig_last_price[i] for i in rand_indices]

# split data into train, test and validation sets
i_50p = len(X) / 2
i_75p = len(X) * 3 / 4

X_train = X[:i_50p]
y_train = y[:i_50p]
X_last_price_train = X_last_price[:i_50p]

X_test = X[i_50p:i_75p]
y_test = y[i_50p:i_75p]
X_last_price_test = X_last_price[i_50p:i_75p]

X_cv = X[i_75p:]
y_cv = y[i_75p:]
X_last_price_cv = X_last_price[i_75p:]

# fit with ordinary linear reg
model = linear_model.Ridge(normalize=True, alpha=ALPHA)
model.fit(X_train, y_train)

# map predicted and actual changes into vectors to easily calculate performance
predicted_prices_train = [model.predict([x])[0] for x in X_train]
predicted_changes_train = [predicted_prices_train[i] - X_last_price_train[i]
                           for i in xrange(len(X_train))]
actual_changes_train = [y_train[i] - X_last_price_train[i]
                        for i in xrange(len(X_train))]

predicted_prices_test = [model.predict([x])[0] for x in X_test]
predicted_changes_test = [predicted_prices_test[i] - X_last_price_test[i]
                          for i in xrange(len(X_test))]
actual_changes_test = [y_test[i] - X_last_price_test[i]
                       for i in xrange(len(X_test))]

# calc and output model performance
train_perf = scoring.by_change_direction(
    predicted_changes_train, actual_changes_train)
test_perf = scoring.by_change_direction(
    predicted_changes_test, actual_changes_test)

print 'training performance: {0}/{1} = {2:.2f}%'.format(
    train_perf, len(X_train),
    float(train_perf) / len(X_train) * 100)

print 'test performance: {0}/{1} = {2:.2f}%'.format(
    test_perf, len(X_test),
    float(test_perf) / len(X_test) * 100)
