"""
various model scoring strategy
all strategy takes a prediction and a true output vector
the vectors must have the same length to behave properly
"""


def by_class(predictions, labels, threshold=0.5):
    """
    scoring by class equality
    ignores prediction if confidence is lower than threshold
    """

    total = 0
    score = 0

    for predicted_probs, label in zip(predictions, labels):
        class1_prob = predicted_probs[1]
        if class1_prob >= threshold:
            total += 1
            if label == 1:
                score += 1

    return score, total


def by_change_direction(predicted_changes, actual_changes):
    """
    a simple scoring strategy that looks at the price change direction
    """
    def is_same_direction(data):
        """
        returns true if the predicted change and real change has the same sign
        """
        [predicted_change, actual_change] = data
        return predicted_change * actual_change >= 0
    return len(filter(is_same_direction, zip(predicted_changes, actual_changes)))
