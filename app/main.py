import streamlit as st
import sys
import os

# Ajouter le dossier parent (racine du projet) au path pour que Python trouve portfolio_module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules
from single_asset import run_single_asset_app            # Quant A
from portfolio_module.dashboard import run_portfolio_app  # Quant B

def main():
    # Config page
    st.set_page_config(
        page_title="Quant Dashboard - Python / Git / Linux",
        layout="wide"
    )

    # Titre principal
    st.title("Quant Dashboard – Python / Git / Linux")
    st.markdown("Plateforme de recherche quantitative avec données financières (quasi) temps réel.")

    # Sidebar : choix du module
    st.sidebar.title("Navigation")
    module = st.sidebar.radio(
        "Choisir un module :",
        ("Single Asset (Quant A)", "Portfolio (Quant B)")
    )

    # Lancer le module choisi
    if module == "Single Asset (Quant A)":
        run_single_asset_app()
    else:
        run_portfolio_app()

if __name__ == "__main__":
    main()
