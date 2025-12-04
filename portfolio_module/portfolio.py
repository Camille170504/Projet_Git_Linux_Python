import numpy as np

class Portfolio:
    def __init__(self, data, weights):
        self.data = data
        self.weights = np.array(weights)

    def cumulative_value(self):
        returns = self.data.pct_change().fillna(0)
        weighted_returns = returns @ self.weights
        return (1 + weighted_returns).cumprod()
