import matplotlib.pyplot as plt

def plot_assets(data):
    data.plot(title="Prix des actifs")
    plt.show()

def plot_portfolio(cumulative_value):
    cumulative_value.plot(title="Valeur cumulative du portefeuille")
    plt.show()
