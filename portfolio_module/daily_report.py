from portfolio_module.data import get_data
from portfolio_module.portfolio import Portfolio
from portfolio_module.metrics import calculate_metrics
import pandas as pd
from datetime import datetime

assets = ["AAPL", "GOOGL", "MSFT"]
weights = [0.4, 0.4, 0.2]

df = get_data(assets)
portfolio = Portfolio(df, weights)
metrics = calculate_metrics(df, weights)

report_file = f"/home/user/reports/daily_report_{datetime.today().strftime('%Y-%m-%d')}.csv"
pd.DataFrame(metrics).to_csv(report_file)
print(f"Rapport sauvegardé : {report_file}")
