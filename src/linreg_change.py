"""
warm up #2 - simple linear regression to predict price change
model looks at the n days history of price change, then predicts
next days price change; scoring does not care about the magnitude
of the change but only the direction of the change (+ or -)
"""

from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

import scoring
from data.loader import Loader
from data.splitter import split

# args
TICKER = 'FB'
DAYS = 20
DEGREE = 2
ALPHA = 0.1

# load price change data
loader = Loader('tmp/prices_all.db')
X, y = loader.load_change_history(TICKER, DAYS)

# add polynomial features
poly = PolynomialFeatures(degree=DEGREE)
poly.fit(X)
X = poly.transform(X)

# shuffle and split data
X_train, y_train, X_test, y_test, X_cv, y_cv = split(X, y, shuffle=True)

# fit linear regression model with regularization
# model = linear_model.BayesianRidge(normalize=True, alpha_1=ALPHA, alpha_2=ALPHA)
model = linear_model.Ridge(normalize=True, alpha=ALPHA)
model.fit(X_train, y_train)

# make predictions on training and test for scoring
predictions_train = [model.predict([x])[0] for x in X_train]
predictions_test = [model.predict([x])[0] for x in X_test]
predictions_cv = [model.predict([x])[0] for x in X_cv]

# score the model
score_train = scoring.by_change_direction(predictions_train, y_train)
score_test = scoring.by_change_direction(predictions_test, y_test)
score_cv = scoring.by_change_direction(predictions_cv, y_cv)

print 'training performance: {0}/{1} = {2:.2f}%'.format(
    score_train, len(y_train),
    float(score_train) / len(y_train) * 100)

print 'test performance: {0}/{1} = {2:.2f}%'.format(
    score_test, len(y_test),
    float(score_test) / len(y_test) * 100)

print 'validation performance: {0}/{1} = {2:.2f}%'.format(
    score_cv, len(y_cv),
    float(score_cv) / len(y_cv) * 100)
