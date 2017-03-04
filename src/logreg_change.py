"""
warm up #3 - simple logistic regression to predict price change

update #1 - good accuracy but again, probably because i was using
well known stocks to test, will need more testing
"""

import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

from data.loader import load, load_history
from data.splitter import split

# args
TICKER = 'MSFT'
DAYS_HISTORY = 252
DAYS_FUTURE = 252
DEGREE = 1
C = 1.0 / 30.0

# load price data
df = load(TICKER)

# only use most recent 5 years of data
df = df[-252 * 5:]

# load price change history
df_price_change_history = load_history(TICKER, 'change', DAYS_HISTORY)

# load volume history
df_volume_history = load_history(TICKER, 'volume', DAYS_HISTORY)

# series for price change n days to the future
change_future = (df['close'].shift(-DAYS_FUTURE) -
                 df['close']) / df['close'] * 100
change_future.name = 'change_future'

# build data frame and drop empty rows
X = df_price_change_history.join(
    df_volume_history).join(change_future).dropna()

# shuffle data frame
X = X.reindex(np.random.permutation(X.index))

# get y and map into proper log regression output
y = X.pop('change_future')
y = [1 if change > 0 else 0 for change in y]

# add polynomial terms to X
poly = PolynomialFeatures(degree=DEGREE, interaction_only=False)
poly.fit(X)
X = poly.transform(X)

# scale features X
scale = StandardScaler()
scale.fit(X)
X = scale.transform(X)

# shuffle and split data
X_train, y_train, X_test, y_test, X_cv, y_cv = split(X, y)

# fit linear regression model with regularization
# model = linear_model.BayesianRidge(normalize=True, alpha_1=ALPHA, alpha_2=ALPHA)
model = linear_model.LogisticRegression(C=C)
model.fit(X_train, y_train)

# score predictions
def score(predictions, labels):
    """score predictions by labels"""
    positives = [1 if item[0] == item[1]
                 else 0 for item in zip(predictions, labels)]
    return sum(positives)

score_train = score(model.predict(X_train), y_train)
print '{0}/{1} {2:.2f}%'.format(score_train,
                                len(y_train),
                                float(score_train) / len(y_train) * 100)

score_test = score(model.predict(X_test), y_test)
print '{0}/{1} {2:.2f}%'.format(score_test,
                                len(y_test),
                                float(score_test) / len(y_test) * 100)

score_cv = score(model.predict(X_cv), y_cv)
print '{0}/{1} {2:.2f}%'.format(score_cv,
                                len(y_cv),
                                float(score_cv) / len(y_cv) * 100)
