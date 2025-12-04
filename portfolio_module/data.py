import pandas as pd
import requests
from datetime import datetime

BINANCE_BASE_URL = "https://api.binance.com"

def fetch_single_asset_history(symbol: str, start: str, end: str, interval: str = "1h") -> pd.DataFrame:
    """Récupère l'historique d'un seul actif (même code que Quant A)."""
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)
    delta_hours = max(1, int((end_dt - start_dt).total_seconds() // 3600))
    limit = min(delta_hours, 1000)

    url = f"{BINANCE_BASE_URL}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[fetch_single_asset_history] Erreur API Binance: {e}")
        return pd.DataFrame()

    raw_klines = resp.json()
    if not raw_klines:
        return pd.DataFrame()

    dates, closes = [], []
    for k in raw_klines:
        dt = datetime.utcfromtimestamp(k[0] / 1000.0)
        dates.append(dt)
        closes.append(float(k[4]))

    df = pd.DataFrame({symbol: closes}, index=pd.to_datetime(dates))
    df.sort_index(inplace=True)
    return df

def get_data(symbols, start: str, end: str, interval: str = "1h") -> pd.DataFrame:

    """
    Récupère l'historique de plusieurs actifs et fusionne dans un DataFrame.
    """
    dfs = []
    for sym in symbols:
        df = fetch_single_asset_history(sym, start, end, interval)
        if not df.empty:
            dfs.append(df)
    
    if not dfs:
        return pd.DataFrame()
    
    # Merge par index (date)
    df_all = pd.concat(dfs, axis=1)
    df_all.sort_index(inplace=True)
    return df_all

# Exemple d'utilisation
if __name__ == "__main__":
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    df_portfolio = fetch_multi_assets(symbols, start="2025-01-01", end="2025-12-01")
    print(df_portfolio.tail())
