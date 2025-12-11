import pandas as pd
import requests
from datetime import datetime

BINANCE_BASE_URL = "https://api.binance.com"


def fetch_single_asset_history(
    symbol: str,
    start: str,
    end: str,
    interval: str = "1h",
) -> pd.DataFrame:
    """
    Récupère l'historique d'une crypto depuis l'API publique de Binance.

    - symbol : "BTCUSDT", "ETHUSDT", ...
    - interval : "1m", "5m", "1h", "4h", "1d", ...
    """

    # Calcul du nombre de points (limite API Binance = 1000)
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)
    delta_hours = max(1, int((end_dt - start_dt).total_seconds() // 3600))
    limit = min(delta_hours, 1000)

    url = f"{BINANCE_BASE_URL}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[fetch_single_asset_history] Erreur API Binance: {e}")
        return pd.DataFrame()

    raw_klines = resp.json()
    if not raw_klines:
        return pd.DataFrame()

    dates = []
    closes = []

    # Structure des klines Binance :
    # [ openTime, open, high, low, close, volume, closeTime, ... ]
    for k in raw_klines:
        open_time_ms = k[0]
        close_price = float(k[4])
        dt = datetime.utcfromtimestamp(open_time_ms / 1000.0)
        dates.append(dt)
        closes.append(close_price)

    df = pd.DataFrame({"date": dates, "price": closes})
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)
    return df


def fetch_multi_assets_history(
    symbols: list[str],
    start: str,
    end: str,
    interval: str = "1h",
) -> pd.DataFrame:
    """
    Récupère l'historique de plusieurs cryptos depuis Binance.
    Retourne un DataFrame avec une colonne par symbole.
    """

    all_dfs = []

    for sym in symbols:
        df_sym = fetch_single_asset_history(sym, start, end, interval)
        if df_sym.empty:
            continue
        df_sym = df_sym.rename(columns={"price": sym})
        all_dfs.append(df_sym)

    if not all_dfs:
        return pd.DataFrame()

    # jointure sur les dates communes
    df_all = pd.concat(all_dfs, axis=1, join="inner")
    return df_all
