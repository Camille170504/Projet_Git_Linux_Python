import streamlit as st
from single_asset import run_single_asset_app
from portfolio import run_portfolio_app

def main():
    st.set_page_config(
        page_title="Quant Dashboard - Python / Git / Linux",
        layout="wide"
    )

    st.title("Quant Dashboard – Python / Git / Linux")
    st.markdown("Plateforme de **recherche quantitative** avec données financières (quasi) temps réel.")

    # Sidebar : choix du module
    st.sidebar.title("Navigation")
    module = st.sidebar.radio(
        "Choisir un module :",
        ("Single Asset (Quant A)", "Portfolio (Quant B)")
    )

    if module == "Single Asset (Quant A)":
        run_single_asset_app()
    else:
        run_portfolio_app()

if __name__ == "__main__":
    main()
