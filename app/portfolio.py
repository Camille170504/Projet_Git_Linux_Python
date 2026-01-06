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
    st.header("Portfolio Module – Quant B")

    st.sidebar.subheader("Portfolio settings")

    # Liste de cryptos disponibles
    crypto_choices = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]

    symbols = st.sidebar.multiselect(
        "Choose the cryptocurrencies for your portfolio",
        options=crypto_choices,
        default=["BTCUSDT", "ETHUSDT", "SOLUSDT"],
        help="Select at least two assets for a true diversification effect."
    )

    if len(symbols) < 2:
        st.warning("Select at least two cryptocurrencies.")
        return

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start date", value=pd.Timestamp.today()-pd.DateOffset(years=1)
    with col2:
        end_date = st.date_input("End date", value=pd.Timestamp.today())

    if start_date >= end_date:
        st.error("The start date must be strictly before the end date.")
        return

    # ---------- DATA RECOVERY ----------
    df_prices = fetch_multi_assets_history(
        symbols=symbols,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d")
    )
    df_prices.index = pd.to_datetime(df_prices.index)

    df_prices = df_prices.loc[
        (df_prices.index >= pd.to_datetime(start_date)) &
        (df_prices.index <= pd.to_datetime(end_date))
    ]

    if df_prices.empty:
        st.warning("No data is available for this period and these assets.")
        return

    # ---------- PRICE CHART (NORMALIZED) ----------
    st.subheader("Normalized price evolution of selected assets (base 100)")

    df_prices_norm = 100 * df_prices / df_prices.iloc[0]
    st.line_chart(df_prices_norm)

    st.caption(
        "Prices are normalized to base 100 to allow comparison between assets "
        "with very different price levels."
    )

    # ---------- RETURNS & PORTFOLIO ----------
    df_returns = df_prices.pct_change().dropna()
    if df_returns.empty:
        st.warning("Not enough data to calculate returns.")
        return

    n_assets = len(symbols)
    weights = pd.Series(1.0 / n_assets, index=symbols)

    st.markdown(
        f"**Equal weighting** : {', '.join([f'{s} {1/n_assets:.2%}' for s in symbols])}"
    )

    portfolio_returns = (df_returns * weights).sum(axis=1)
    portfolio_cum_value = compute_cumulative_value(
        portfolio_returns, initial_capital=1.0
    )

    # ---------- PORTFOLIO VALUE ----------
    st.subheader("Cumulative portfolio value")
    st.line_chart(portfolio_cum_value)

    # ---------- KPIs ----------
    perf_totale = total_return(portfolio_cum_value) * 100
    vol_annuelle = annualized_volatility(portfolio_returns) * 100
    mdd = max_drawdown(portfolio_cum_value) * 100
    sharpe = sharpe_ratio(portfolio_returns)

    st.subheader("Portfolio performance indicators")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total performance", f"{perf_totale:.2f} %")
    c2.metric("Annualized volatility", f"{vol_annuelle:.2f} %")
    c3.metric("Max drawdown", f"{mdd:.2f} %")
    c4.metric("Sharpe ratio", f"{sharpe:.2f}")

    # ---------- CORRELATION ----------
    st.subheader("Return correlation matrix")
    corr = df_returns.corr()
    st.dataframe(corr.style.format("{:.2f}"))
