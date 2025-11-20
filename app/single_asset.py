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

# ---------- Stratégie Moving Average (MA) ----------

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
    st.header("Module Single Asset – Quant A")

    st.markdown(
        """
        Suivi d'une cryptomonnaie en temps quasi réel grâce aux données Binance.

        Visualisez le prix, la stratégie choisie (*Buy & Hold* ou *Moving Average*)
        et des indicateurs clés (volatilité, Sharpe ratio, drawdown…).
        """
    )

    # --- Sidebar : paramètres ---
    st.sidebar.subheader("Paramètres Single Asset")

    # Menu déroulant pour choisir la crypto
    crypto_choices = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
    symbol = st.sidebar.selectbox(
        "Crypto (Binance)",
        options=crypto_choices,
        index=0,
        help="Paires spot USDT disponibles sur Binance (ex : BTCUSDT)."
    )

    # Choix de la stratégie
    strategy = st.sidebar.radio(
        "Stratégie",
        options=["Buy & Hold", "Moving Average (MA)"],
        index=0,
    )

    # Paramètres pour la stratégie MA
    short_window = None
    long_window = None
    if strategy == "Moving Average (MA)":
        st.sidebar.markdown("**Paramètres Moving Average**")
        short_window = st.sidebar.slider(
            "MA courte (périodes)",
            min_value=5,
            max_value=100,
            value=20,
            step=1,
        )
        long_window = st.sidebar.slider(
            "MA longue (périodes)",
            min_value=10,
            max_value=200,
            value=50,
            step=1,
        )
        if short_window >= long_window:
            st.sidebar.error("La MA courte doit être strictement inférieure à la MA longue.")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Date de début", value=pd.to_datetime("2024-10-10"))
    with col2:
        end_date = st.date_input("Date de fin", value=pd.to_datetime("2024-11-20"))

    if start_date >= end_date:
        st.error("La date de début doit être strictement avant la date de fin.")
        return

    # ---------- RÉCUPÉRATION DES DONNÉES ----------
    df = fetch_single_asset_history(
        symbol=symbol,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d")
    )

    if df.empty:
        st.warning("Aucune donnée disponible pour cette période.")
        return

    # ---------- GRAPHIQUE DE PRIX ----------
    st.subheader(f"Prix de l'actif : {symbol}")
    st.line_chart(df["price"])

    # ---------- CHOIX DE LA STRATÉGIE ----------
    # Rendements de base de l'actif (pour Buy & Hold)
    asset_returns = compute_returns(df["price"])
    if asset_returns.empty:
        st.warning("Pas assez de données pour calculer les rendements.")
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
            st.warning("Pas assez de données pour la stratégie Moving Average.")
            return

    # Valeur cumulée de la stratégie choisie
    cum_value = compute_cumulative_value(strat_returns, initial_capital=1.0)

    st.subheader(f"Stratégie {strat_name} – Valeur cumulée")
    st.line_chart(cum_value)

    # ---------- KPIs ----------
    perf_totale = total_return(cum_value) * 100
    vol_annuelle = annualized_volatility(strat_returns) * 100
    mdd = max_drawdown(cum_value) * 100
    sharpe = sharpe_ratio(strat_returns)

    st.subheader("Indicateurs de performance")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Perf totale", f"{perf_totale:.2f} %")
    col2.metric("Vol annualisée", f"{vol_annuelle:.2f} %")
    col3.metric("Max drawdown", f"{mdd:.2f} %")
    col4.metric("Sharpe ratio", f"{sharpe:.2f}")

    st.caption("Données Binance + stratégie sélectionnée sur la période choisie.")

