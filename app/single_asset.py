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

# ---------- Moving Average Strategy (MA) ----------

def moving_average_strategy_returns(
    price: pd.Series,
    short_window: int = 20,
    long_window: int = 50,
) -> pd.Series:

    """
    Stratégie simple de croisement de moyennes mobiles :
    - long quand MA courte > MA longue
    - cash sinon

    Retourne une série de rendements de la stratégie.
    """
    short_ma = price.rolling(short_window).mean()
    long_ma = price.rolling(long_window).mean()

    # Signal : 1 = investi, 0 = cash
    signal = (short_ma > long_ma).astype(int)

    # On décale d'une période pour éviter le look-ahead bias
    signal = signal.shift(1).fillna(0)

    # Rendements de l'actif
    returns = price.pct_change().fillna(0)

    # Rendements de la stratégie
    strat_returns = signal * returns

    return strat_returns.dropna()


# ---------- App Single Asset ----------

def run_single_asset_app():
    st.header("Single Asset Module – Quant A")

    # --- Sidebar ---
    st.sidebar.subheader("Single Asset Settings")

    # Drop-down menu to choose the crypto
    crypto_choices = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
    symbol = st.sidebar.selectbox(
        "Crypto (Binance)",
        options=crypto_choices,
        index=0,
        help="Paires spot USDT disponibles sur Binance."
    )

    # Strategy selection
    strategy = st.sidebar.radio(
        "Strategy",
        options=["Buy & Hold", "Moving Average (MA)"],
        index=0,
    )

    # Settings for the MA strategy
    short_window = None
    long_window = None
    if strategy == "Moving Average (MA)":
        st.sidebar.markdown("**Moving Average Settings**")
        short_window = st.sidebar.slider(
            "MA short (periods)",
            min_value=5,
            max_value=100,
            value=20,
            step=1,
        )
        long_window = st.sidebar.slider(
            "MA long (periods)",
            min_value=10,
            max_value=200,
            value=50,
            step=1,
        )
        if short_window >= long_window:
            st.sidebar.error("The short MA must be strictly less than the long MA.")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start date", value=pd.Timestamp.today()-pd.DateOffset(years=1))
    with col2:
        end_date = st.date_input("End date", value=pd.Timestamp.today())

    if start_date >= end_date:
        st.error("The start date must be strictly before the end date.")
        return

    # ---------- DATA RECOVERY ----------
    df = fetch_single_asset_history(
        symbol=symbol,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d")
    )

    if df.empty:
        st.warning("No data is available for this period.")
        return

    # ---------- PRICE CHART ----------
    st.subheader(f" Asset price : {symbol}")
    st.line_chart(df["price"])

    # ---------- CHOICE OF STRATEGY ----------
    asset_returns = compute_returns(df["price"])
    if asset_returns.empty:
        st.warning("Not enough data to calculate yields.")
        return

    if strategy == "Buy & Hold":
        strat_name = "Buy & Hold"
        strat_returns = asset_returns
    else:
        strat_name = f"Moving Average ({short_window}/{long_window})"
        strat_returns = moving_average_strategy_returns(
            df["price"],
            short_window=short_window,
            long_window=long_window,
        )

        if strat_returns.empty:
            st.warning("Not enough data for the Moving Average strategy.")
            return

    cum_value = compute_cumulative_value(strat_returns, initial_capital=1.0)

    # ---------- GRAPHIQUE COMBINÉ ----------
    st.subheader(f"Prix & stratégie {strat_name}")

 # On met la stratégie sur la même échelle que le prix pour la lisibilité
    # (affichage uniquement : les KPIs restent calculés sur cum_value brute)
    first_price = df.loc[cum_value.index[0], "price"]
    first_cum = cum_value.iloc[0]
    strategy_scaled = cum_value * (first_price / first_cum)


    df_plot = pd.DataFrame({
        "Price": df.loc[cum_value.index, "price"],
        "Strategy value": cum_value,
    })

    st.line_chart(df_plot)
    st.subheader(f"Strategy {strat_name} – Cumulative value")
    st.line_chart(cum_value)

    # ---------- KPIs ----------
    perf_totale = total_return(cum_value) * 100
    vol_annuelle = annualized_volatility(strat_returns) * 100
    mdd = max_drawdown(cum_value) * 100
    sharpe = sharpe_ratio(strat_returns)

    st.subheader("Performance indicators")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total performance", f"{perf_totale:.2f} %")
    col2.metric("Annualized volatility", f"{vol_annuelle:.2f} %")
    col3.metric("Max drawdown", f"{mdd:.2f} %")
    col4.metric("Sharpe ratio", f"{sharpe:.2f}")

    st.caption("Données Binance + stratégie sélectionnée sur la période choisie.")
