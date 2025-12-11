import pandas as pd
import streamlit as st

from data_loader import fetch_multi_assets_history
from metrics import (
    compute_returns,
    compute_cumulative_value,
    max_drawdown,
    annualized_volatility,
    total_return,
    sharpe_ratio,
)

def run_portfolio_app():
    st.header("Module Portfolio – Quant B")

    st.markdown(
        """
        Analyse d'un **portefeuille de plusieurs cryptos** (données Binance).

        On construit un portefeuille pondéré également et on calcule :
        - la valeur cumulée,
        - la volatilité,
        - le max drawdown,
        - le Sharpe ratio,
        - la matrice de corrélation des actifs.
        """
    )

    st.sidebar.subheader("Paramètres Portfolio")

    # Liste de cryptos disponibles
    crypto_choices = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]

    symbols = st.sidebar.multiselect(
        "Choisir les cryptos du portefeuille",
        options=crypto_choices,
        default=["BTCUSDT", "ETHUSDT", "SOLUSDT"],
        help="Sélectionne au moins deux actifs pour un vrai effet de diversification."
    )

    if len(symbols) == 0:
        st.warning("Sélectionne au moins une crypto.")
        return

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Date de début", value=pd.to_datetime("2024-10-10"))
    with col2:
        end_date = st.date_input("Date de fin", value=pd.to_datetime("2024-11-20"))

    if start_date >= end_date:
        st.error("La date de début doit être strictement avant la date de fin.")
        return

    # ---------- RÉCUPÉRATION DES DONNÉES ----------
    df_prices = fetch_multi_assets_history(
        symbols=symbols,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d")
    )

    if df_prices.empty:
        st.warning("Aucune donnée disponible pour cette période et ces actifs.")
        return

    st.subheader("Prix des actifs sélectionnés")
    st.line_chart(df_prices)

    # ---------- RENDEMENTS & PORTEFEUILLE ----------
    df_returns = df_prices.pct_change().dropna()
    if df_returns.empty:
        st.warning("Pas assez de données pour calculer les rendements.")
        return

    # pondération égale
    n_assets = len(symbols)
    weights = pd.Series([1.0 / n_assets] * n_assets, index=symbols)

    st.markdown(f"**Pondération égale** : {', '.join([f'{s} {1/n_assets:.2%}' for s in symbols])}")

    # rendement du portefeuille
    portfolio_returns = (df_returns * weights).sum(axis=1)

    # valeur cumulée du portefeuille
    portfolio_cum_value = compute_cumulative_value(portfolio_returns, initial_capital=1.0)

    st.subheader("Valeur cumulée du portefeuille")
    st.line_chart(portfolio_cum_value)

    # ---------- KPIs ----------
    perf_totale = total_return(portfolio_cum_value) * 100
    vol_annuelle = annualized_volatility(portfolio_returns) * 100
    mdd = max_drawdown(portfolio_cum_value) * 100
    sharpe = sharpe_ratio(portfolio_returns)

    st.subheader("Indicateurs de performance du portefeuille")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Perf totale", f"{perf_totale:.2f} %")
    c2.metric("Vol annualisée", f"{vol_annuelle:.2f} %")
    c3.metric("Max drawdown", f"{mdd:.2f} %")
    c4.metric("Sharpe ratio", f"{sharpe:.2f}")

    # ---------- Corrélation ----------
    st.subheader("Matrice de corrélation des rendements")
    corr = df_returns.corr()
    st.dataframe(corr.style.format("{:.2f}"))
