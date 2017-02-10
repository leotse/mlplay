# warm up - simple linear regression on price data

# findings: linear regression even with polynomial features performs quite
# poorly in general; which is expected as it is hard to imagine linear
# models can successfully model market dynamics; model was able to find
# signal in some stocks but requires special sets of hyper parameters

# insights: in the final system it's very likely that individual stocks
# will need their own set of hyper parameters to work well

import random

import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

from data.loader import Loader

# stock to train
ticker = 'SBUX'

# hyper parameters
n = 5
degree = 3
alpha = 0.0001
y_field = 'adj_close'
x_fields = ['adj_open', 'adj_high', 'adj_low',
            'adj_close', 'adj_volume', 'split_ratio']

# load price data
loader = Loader('tmp/prices_all.db')
X, y = loader.n_days_history(ticker,
                             n=n,
                             x_fields=x_fields,
                             y_field=y_field)

# add polynomial features
poly = PolynomialFeatures(degree=degree)
poly.fit(X)
X = poly.transform(X)

# shuffle X and y
rand_indices = random.sample(list(range(len(X))), len(X))
X = [X[i] for i in rand_indices]
y = [y[i] for i in rand_indices]

# split data into train, test and validation sets
i_50p = len(X) / 2
i_75p = len(X) / 4 * 3
X_train = X[:i_50p]
y_train = y[:i_50p]
X_test = X[i_50p:i_75p]
y_test = y[i_50p:i_75p]
X_cv = X[i_75p:]
y_cv = y[i_75p:]

# fit with ordinary linear reg
# model = linear_model.LinearRegression(normalize=True)
model = linear_model.Ridge(normalize=True, alpha=alpha)
model.fit(X_train, y_train)

# test performance
positives = 0
X_test = X_train
y_test = y_train

for x, y in zip(X_test, y_test):
    prediction = model.predict([x])
    if(np.sign(prediction) == np.sign(y)):
        positives += 1

print 'performance: {0}/{1} = {2:.2f}%'.format(
    positives,
    len(X_test),
    float(positives) / len(X_test) * 100
)
