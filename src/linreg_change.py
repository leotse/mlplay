"""
warm up #2 - simple linear regression to predict price change
model looks at the n days history of price change, then predicts
next days price change; scoring does not care about the magnitude
of the change but only the direction of the change (+ or -)

update #1 - added argument to predict n days in the future instead of
always looking at the immediate next day; accuracy is surprisingly high
but this is probably just caused by the bias of picking well known stocks
"""

import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

import scoring
from data.loader import load, load_history
from data.splitter import split

# args
TICKER = 'FB'
DAYS_HISTORY = 252
DAYS_FUTURE = 252
DEGREE = 1
ALPHA = 3.0

# load price data
df = load(TICKER)

# we only want to look at the most recent 5 years of data
df = df[-252 * 5:]

# load price change history
# collapses n days history into one row
# will be used as input matrix X
df_change_history = load_history(TICKER, 'change', DAYS_HISTORY)

# load volume
df_volume_history = load_history(TICKER, 'volume', DAYS_HISTORY)

# calculate total change 10 days in the future
# will be used as label vector y
change_future = (df['close'].shift(-DAYS_FUTURE) - df['close']) / df['close'] * 100.0
change_future.name = 'change_future'

# line up data and drop any na values
X = df_change_history.join(df_volume_history).join(change_future).dropna()

# shuffle data frame
X = X.reindex(np.random.permutation(X.index))

# separate out label vector y
y = X.pop('change_future')

# init polynomial feature transformer
poly = PolynomialFeatures(degree=DEGREE, interaction_only=False)
poly.fit(X)
X = poly.transform(X)

# scale input data
scaleX = StandardScaler()
scaleX.fit(X)
X = scaleX.transform(X)

# split training, test and validation set
X_train, y_train, X_test, y_test, X_cv, y_cv = split(X, y)

# fit linear regression model
model = linear_model.Ridge(alpha=ALPHA)
model.fit(X_train, y_train)

# score predictions
score_train = scoring.by_change_direction(model.predict(X_train), y_train)
print '{0}/{1} {2:.2f}%'.format(score_train,
                                len(y_train),
                                float(score_train)/len(y_train) * 100)

score_test = scoring.by_change_direction(model.predict(X_test), y_test)
print '{0}/{1} {2:.2f}%'.format(score_test,
                                len(y_test),
                                float(score_test)/len(y_test) * 100)

score_cv = scoring.by_change_direction(model.predict(X_cv), y_cv)
print '{0}/{1} {2:.2f}%'.format(score_cv,
                                len(y_cv),
                                float(score_cv)/len(y_cv) * 100)
