import streamlit as st
from single_asset import run_single_asset_app


def main():
    # Page configuration
    st.set_page_config(
        page_title="Quant Dashboard",
        layout="wide",
    )

    # Main title
    st.title("Quant Dashboard")

    # No navigation menu here: only the Single Asset module
    run_single_asset_app()


if __name__ == "__main__":
    main()
