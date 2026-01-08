import numpy as np
import pandas as pd

def compute_returns(price_series: pd.Series) -> pd.Series:
    return price_series.pct_change().dropna()

def compute_cumulative_value(returns: pd.Series, initial_capital: float = 1.0) -> pd.Series:
    return initial_capital * (1 + returns).cumprod()

def max_drawdown(cum_value: pd.Series) -> float:
    running_max = cum_value.cummax()
    drawdown = (cum_value - running_max) / running_max
    return float(drawdown.min())

def annualized_volatility(returns: pd.Series, freq: int = 252) -> float:
    """Vol annualisée (freq=252 pour jours de bourse)."""
    return float(returns.std() * np.sqrt(freq))

def total_return(cum_value: pd.Series) -> float:
    """Performance totale entre début et fin, en %."""
    return float(cum_value.iloc[-1] / cum_value.iloc[0] - 1)

def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0, freq: int = 252) -> float:
    """Sharpe ratio annualisé (rf en taux annuel)."""
    excess_returns = returns - risk_free_rate / freq
    vol = annualized_volatility(excess_returns, freq=freq)
    if vol == 0:
        return np.nan
    return float((excess_returns.mean() * freq) / vol)
