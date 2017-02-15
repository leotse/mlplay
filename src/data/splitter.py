"""Data spliting utils"""

import random


def split(X, y, shuffle=False):
    """
    takes a data set and splits it into training (50%),
    test (25%) and validation (25%) set
    with option to shuffle the data
    """

    if shuffle:
        rand_indices = random.sample(list(range(len(X))), len(X))
        X = [X[i] for i in rand_indices]
        y = [y[i] for i in rand_indices]

    total = len(X)
    i_50 = total / 2
    i_75 = total * 3 / 4

    X_training = X[:i_50]
    y_training = y[:i_50]

    X_test = X[i_50:i_75]
    y_test = y[i_50:i_75]

    X_cv = X[i_75:]
    y_cv = y[i_75:]

    return X_training, y_training, X_test, y_test, X_cv, y_cv
