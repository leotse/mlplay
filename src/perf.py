# performance evaluations - takes a model, X and y
# returns the training and test performance of the model

# simple evaluation that only looks at the sign of the prediction
def simple(model, X, y):
    def is_positive(row):
        [x, y] = row
        prediction = model.predict([x])
        return prediction * y > 0
    return len(filter(is_positive,  zip(X, y)))