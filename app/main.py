import streamlit as st
from single_asset import run_single_asset_app
from portfolio import run_portfolio_app


def main():
    st.set_page_config(
        page_title="Quant Dashboard",
        layout="wide",
    )

    st.experimental_autorefresh(interval=300_000, key="auto_refresh")
    st.title("Quant Dashboard – Crypto")
    st.markdown(
        "Quantitative research platform with near real-time Binance data."
    )

    # Sidebar : navigation
    st.sidebar.title("Navigation")
    module = st.sidebar.radio(
        "Choose a module :",
        ("Single Asset (Quant A)", "Portfolio (Quant B)"),
    )

    # Routing to sub-modules
    if module == "Single Asset (Quant A)":
        run_single_asset_app()
    else:
        run_portfolio_app()


if __name__ == "__main__":
    main()
