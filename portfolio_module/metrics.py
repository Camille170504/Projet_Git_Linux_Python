def calculate_metrics(data, weights):
    returns = data.pct_change().fillna(0)
    port_returns = returns @ weights
    metrics = {
        "mean_return": port_returns.mean(),
        "volatility": port_returns.std(),
        "max_drawdown": (port_returns.cumprod().cummax() - port_returns.cumprod()).max(),
        "correlation_matrix": returns.corr()
    }
    return metrics
