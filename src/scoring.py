"""
various model scoring strategy
all strategy takes a prediction and a true output vector
the vectors must have the same length to behave properly
"""


def change_direction(predicted_changes, actual_changes):
    """
    a simple scoring strategy that looks at the price change direction
    """
    def is_positive(data):
        """
        returns true if the predicted change and real change has the same sign
        """
        [predicted_change, actual_change] = data
        return predicted_change * actual_change >= 0
    return len(filter(is_positive, zip(predicted_changes, actual_changes)))
