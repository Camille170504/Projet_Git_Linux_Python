import pandas as pd
import requests
from datetime import datetime

BINANCE_BASE_URL = "https://api.binance.com"

def fetch_single_asset_history(symbol: str, start: str, end: str, interval: str = "1h") -> pd.DataFrame:
    """
    Récupère l'historique d'une crypto depuis l'API publique de Binance.

    Pour simplifier, on ne passe pas le start/end exact à l'API :
    on calcule seulement un nombre de points (limit) en fonction de la durée.

    - symbol : ex. "BTCUSDT", "ETHUSDT"
    - interval : "1m", "5m", "1h", "4h", "1d"...
    """

    # 1) Calcul d'un nombre approximatif de points à récupérer
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)

    # nombre d'heures entre start et end (min 1, max 1000 pour Binance)
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

    # Structure des klines Binance :
    # [ openTime, open, high, low, close, volume, closeTime, ... ]
    dates = []
    closes = []

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
