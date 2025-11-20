import pandas as pd
import streamlit as st
from data_loader import fetch_single_asset_history

def fetch_single_asset_history(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Pour l'instant : génère des données factices pour tester l'interface.
    On remplacera plus tard par un appel API.
    """
    dates = pd.date_range(start=start, end=end, freq="D")
    # prix fictif : une pente + un peu de bruit
    prices = 100 + (0.2 * range(len(dates)))
    df = pd.DataFrame({"date": dates, "price": prices})
    df.set_index("date", inplace=True)
    return df

