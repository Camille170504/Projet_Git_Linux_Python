import pandas as pd

def fetch_single_asset_history(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Pour l'instant : génère des données factices pour tester l'interface.
    """
    dates = pd.date_range(start=start, end=end, freq="D")
    prices = 100 + 0.2 * pd.Series(range(len(dates)))  # prix fictif
    df = pd.DataFrame({"date": dates, "price": prices})
    df.set_index("date", inplace=True)
    return df
