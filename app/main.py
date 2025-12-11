import streamlit as st
from single_asset import run_single_asset_app


def main():
    # Config de la page
    st.set_page_config(
        page_title="Quant Dashboard – Crypto (Quant A)",
        layout="wide",
    )

    # Titre principal
    st.title("Quant Dashboard – Crypto – Quant A")
    st.markdown(
        "Suivi d'une **cryptomonnaie en temps quasi réel** grâce aux données Binance."
    )

    # Pas de menu de navigation ici : uniquement le module Single Asset
    run_single_asset_app()


if __name__ == "__main__":
    main()
