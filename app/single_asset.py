import pandas as pd
import streamlit as st

from data_loader import fetch_single_asset_history
from metrics import (
    compute_returns,
    compute_cumulative_value,
    max_drawdown,
    annualized_volatility,
    total_return,
    sharpe_ratio,
)

def run_single_asset_app():
    st.header("Module Single Asset – Quant A")

    st.markdown(
        """
        Analyse d'un **actif unique** (action, FX, crypto...).

        Pour l'instant, on affiche des données factices pour tester l'interface.
        """
    )

    # --- Sidebar : paramètres ---
    st.sidebar.subheader("Paramètres Single Asset")

    symbol = st.sidebar.text_input("Ticker / symbole", value="FAKE_ASSET")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Date de début", value=pd.to_datetime("2024-01-01"))
    with col2:
        end_date = st.date_input("Date de fin", value=pd.to_datetime("2024-03-31"))

    if start_date >= end_date:
        st.error("La date de début doit être strictement avant la date de fin.")
        return

    # --- Récupération des données (factices pour l'instant) ---
    df = fetch_single_asset_history(
        symbol=symbol,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d")
    )

    if df.empty:
        st.warning("Aucune donnée disponible pour cette période.")
        return

    # --- Graphique de prix ---
    st.subheader(f"Prix de l'actif : {symbol}")
    st.line_chart(df["price"])

    # ---------- BUY & HOLD ----------
    returns = compute_returns(df["price"])
    if returns.empty:
        st.warning("Pas assez de données pour calculer les rendements.")
        return

    cum_value = compute_cumulative_value(returns, initial_capital=1.0)

    st.subheader("Stratégie Buy & Hold – Valeur cumulée")
    st.line_chart(cum_value)

    # ---------- KPIs ----------
    perf_totale = total_return(cum_value) * 100        # %
    vol_annuelle = annualized_volatility(returns) * 100  # %
    mdd = max_drawdown(cum_value) * 100                # %
    sharpe = sharpe_ratio(returns)

    st.subheader("Indicateurs de performance")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Perf totale", f"{perf_totale:.2f} %")
    col2.metric("Vol annualisée", f"{vol_annuelle:.2f} %")
    col3.metric("Max drawdown", f"{mdd:.2f} %")
    col4.metric("Sharpe ratio", f"{sharpe:.2f}")
    
    st.caption("Données factices + stratégie Buy & Hold. On branchera une vraie API ensuite.")
