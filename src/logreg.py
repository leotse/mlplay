"""
warm up #3 - simple logistic regression to predict price change
"""

from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

import scoring
from data.loader import Loader
from data.splitter import split

# args
TICKER = 'FB'
DAYS = 10
DEGREE = 2
C = 0.9

# load price change data
loader = Loader('tmp/prices_all.db')
X, y = loader.load_change_history(TICKER, DAYS)

# map y into classes
# 0 = negative or no change
# 1 = positive change
y = [1 if change > 0 else 0 for change in y]

# # add polynomial features
poly = PolynomialFeatures(degree=DEGREE)
poly.fit(X)
X = poly.transform(X)

# shuffle and split data
X_train, y_train, X_test, y_test, X_cv, y_cv = split(X, y, shuffle=True)

# fit linear regression model with regularization
# model = linear_model.BayesianRidge(normalize=True, alpha_1=ALPHA, alpha_2=ALPHA)
model = linear_model.LogisticRegression(C=C)
model.fit(X_train, y_train)

# make predictions
predictions_train = model.predict_proba(X_train)
predictions_test = model.predict_proba(X_test)
predictions_cv = model.predict_proba(X_cv)

# score the model
score_train, total_scored_train = scoring.by_class(predictions_train, y_train, threshold=0.5)
score_test, total_scored_test = scoring.by_class(predictions_test, y_test, threshold=0.5)
score_cv, total_scored_cv = scoring.by_class(predictions_cv, y_cv, threshold=0.5)

def print_perf(name, score, total):
    """output model performance"""
    print '{0} performance: {1}/{2} = {3:.2f}%'.format(
        name,
        score,
        total,
        float(score) / total * 100
    )

print_perf('training', score_train, total_scored_train)
print_perf('test', score_test, total_scored_test)
print_perf('validation', score_cv, total_scored_cv)
