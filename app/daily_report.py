# scripts/daily_report.py

import os
import pandas as pd
from datetime import datetime, timedelta

from data_loader import fetch_single_asset_history
from metrics import (
    compute_returns,
    compute_cumulative_value,
    max_drawdown,
    annualized_volatility,
)

# ---------------- CONFIG ----------------
SYMBOL = "BTCUSDT"
INTERVAL = "1h"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

# Date du rapport = jour précédent
end_date = datetime.utcnow().date()
start_date = end_date - timedelta(days=1)

# ---------------- DATA ----------------
df = fetch_single_asset_history(
    symbol=SYMBOL,
    start=start_date.strftime("%Y-%m-%d"),
    end=end_date.strftime("%Y-%m-%d"),
    interval=INTERVAL,
)

if df.empty:
    print("No data retrieved – report not generated.")
    exit()

# ---------------- METRICS ----------------
open_price = df["price"].iloc[0]
close_price = df["price"].iloc[-1]

returns = compute_returns(df["price"])
cum_value = compute_cumulative_value(returns)

volatility = annualized_volatility(returns)
mdd = max_drawdown(cum_value)

# ---------------- REPORT ----------------
report = pd.DataFrame([{
    "date": start_date.strftime("%Y-%m-%d"),
    "asset": SYMBOL,
    "open_price": open_price,
    "close_price": close_price,
    "daily_return_%": (close_price / open_price - 1) * 100,
    "annualized_volatility": volatility,
    "max_drawdown": mdd,
}])

filename = f"report_{start_date.strftime('%Y-%m-%d')}.csv"
report_path = os.path.join(REPORT_DIR, filename)
report.to_csv(report_path, index=False)

print(f"Daily report generated: {report_path}")
