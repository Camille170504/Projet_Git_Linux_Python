import streamlit as st
from portfolio_module.data import get_data
from portfolio_module.portfolio import Portfolio
from portfolio_module.metrics import calculate_metrics

st.title("Dashboard Multi-Asset Portfolio")

assets = st.multiselect("Choisir des actifs", ["AAPL", "GOOGL", "MSFT"], default=["AAPL", "GOOGL"])
weights_input = st.text_input("Poids des actifs séparés par des virgules", "0.4,0.4")

if assets:
    df = get_data(assets)
    weights = [float(w) for w in weights_input.split(",")]
    
    portfolio = Portfolio(df, weights)
    
    st.subheader("Prix des actifs")
    st.line_chart(df)
    
    st.subheader("Valeur cumulative du portefeuille")
    st.line_chart(portfolio.cumulative_value())
    
    st.subheader("Métriques du portefeuille")
    metrics = calculate_metrics(df, weights)
    st.write(metrics)
