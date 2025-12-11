import streamlit as st
from single_asset import run_single_asset_app
from portfolio import run_portfolio_app


def main():
    # Config de la page
    st.set_page_config(
        page_title="Quant Dashboard – Crypto",
        layout="wide",
    )

    # Titre principal
    st.title("Quant Dashboard – Crypto")
    st.markdown(
        "Plateforme de **recherche quantitative** avec données Binance en temps quasi réel."
    )

    # Sidebar : navigation
    st.sidebar.title("Navigation")
    module = st.sidebar.radio(
        "Choisir un module :",
        ("Single Asset (Quant A)", "Portfolio (Quant B)"),
    )

    # Routing vers les sous-modules
    if module == "Single Asset (Quant A)":
        run_single_asset_app()
    else:
        run_portfolio_app()


if __name__ == "__main__":
    main()
