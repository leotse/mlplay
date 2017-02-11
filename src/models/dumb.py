# a model that makes random predictions with distribution Gaussian(0, 1)
# can be used as baseline

import random


class RandomPredictor:

    def __init__(self):
        self.name = 'I am a random predictor, DO NOT trust my predictions'

    def fit(self, X, y):
        return self

    def predict(self, x):
        return random.gauss(0, 1)
