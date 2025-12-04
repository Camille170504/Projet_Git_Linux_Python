import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Ajouter le dossier parent au path pour éviter les erreurs d'import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import des fonctions et classes depuis le module
from portfolio_module.data import get_data
from portfolio_module.portfolio import Portfolio
from portfolio_module.metrics import calculate_metrics

# Titre du dashboard
st.title("Dashboard Multi-Asset Portfolio")

# Sélection des actifs
assets = st.multiselect(
    "Choisir des actifs",
    ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
    default=["BTCUSDT", "ETHUSDT"]
)

# Sélection des dates
start_date = st.date_input("Date de début", value=pd.to_datetime("2025-01-01"))
end_date = st.date_input("Date de fin", value=pd.to_datetime("2025-12-01"))

# Vérification des dates
if start_date >= end_date:
    st.error("La date de début doit être avant la date de fin.")
elif assets:
    # Récupération des données avec start et end
    df = get_data(assets, str(start_date), str(end_date))

    # Affichage des prix des actifs
    st.subheader("Prix des actifs")
    st.line_chart(df)

    # Poids du portefeuille
    weights_input = st.text_input(
        "Poids des actifs séparés par des virgules",
        ",".join([str(round(1/len(assets), 2)) for _ in assets])
    )
    weights = np.array([float(w) for w in weights_input.split(",")])

    # Vérifier que le nombre de poids = nombre d'actifs
    if len(weights) != len(assets):
        weights = np.ones(len(assets)) / len(assets)  # pondération égale
        st.warning("Le nombre de poids ne correspondait pas au nombre d'actifs. Les poids ont été ajustés automatiquement.")

    # Calcul du portefeuille
    portfolio = Portfolio(df, weights)
    st.subheader("Valeur cumulative du portefeuille")
    st.line_chart(portfolio.cumulative_value())

    # Calcul et affichage des métriques
    st.subheader("Métriques du portefeuille")
    metrics = calculate_metrics(df, weights)
    st.write(metrics)

