import streamlit as st
from data_loader import fetch_single_asset_history

def run_single_asset_app():
    st.header("Module Single Asset – Quant A")

    st.markdown(
        """
        Analyse d'un **actif unique** (action, FX, crypto...).

        On commence par afficher une série de prix factice pour tester la structure.
        """
    )

    # --- Sidebar : paramètres ---
    st.sidebar.subheader("Paramètres Single Asset")

    symbol = st.sidebar.text_input("Ticker / symbole", value="FAKE_ASSET")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Date de début", value=pd.to_datetime("2024-01-01"))
    with col2:
        end_date = st.date_input("Date de fin", value=pd.to_datetime("2024-03-31"))

    if start_date >= end_date:
        st.error("La date de début doit être strictement avant la date de fin.")
        return

    # --- Récupération des données (pour l'instant, factices) ---
    df = fetch_single_asset_history(
        symbol=symbol,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d")
    )

    if df.empty:
        st.warning("Aucune donnée disponible pour cette période.")
        return

    st.subheader(f"Prix de l'actif : {symbol}")
    st.line_chart(df["price"])

    st.caption("Données factices pour tester le dashboard. On branchera une vraie API ensuite.")
