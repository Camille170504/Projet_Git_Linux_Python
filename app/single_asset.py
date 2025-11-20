from metrics import (
    compute_returns,
    compute_cumulative_value,
    max_drawdown,
    annualized_volatility,
    total_return,
    sharpe_ratio,
)

st.subheader(f"Prix de l'actif : {symbol}")
st.line_chart(df["price"])

    # --- Buy & hold sur la période sélectionnée ---
    returns = compute_returns(df["price"])
    cum_value = compute_cumulative_value(returns, initial_capital=1.0)

    st.subheader("Stratégie Buy & Hold (valeur cumulée)")
    st.line_chart(cum_value)

    # --- KPIs ---
    perf_totale = total_return(cum_value) * 100      # en %
    vol_annuelle = annualized_volatility(returns) * 100  # en %
    mdd = max_drawdown(cum_value) * 100              # en %
    sharpe = sharpe_ratio(returns)

    st.subheader("Indicateurs de performance")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Perf totale", f"{perf_totale:.2f} %")
    col2.metric("Vol annualisée", f"{vol_annuelle:.2f} %")
    col3.metric("Max drawdown", f"{mdd:.2f} %")
    col4.metric("Sharpe ratio", f"{sharpe:.2f}")
