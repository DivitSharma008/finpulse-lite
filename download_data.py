import pandas as pd
import yfinance as yf
import os
from datetime import date, timedelta

STOCKS = {
    "RELIANCE":   "RELIANCE.NS",
    "TCS":        "TCS.NS",
    "INFY":       "INFY.NS",
    "HDFCBANK":   "HDFCBANK.NS",
    "ICICIBANK":  "ICICIBANK.NS",
    "SBIN":       "SBIN.NS",
    "ITC":        "ITC.NS",
    "LT":         "LT.NS",
    "HINDUNILVR": "HINDUNILVR.NS",
    "KOTAKBANK":  "KOTAKBANK.NS",
}

DATA_DIR = r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\data"
START    = date.today() - timedelta(days=5 * 365)
END      = date.today()

os.makedirs(DATA_DIR, exist_ok=True)

failed  = []
success = []

for name, ticker_symbol in STOCKS.items():
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=START, end=END)

        if df.empty:
            raise ValueError("No data returned — ticker may be delisted or incorrect.")

        df.index = pd.to_datetime(df.index.date)
        df.index.name = "Date"

        save_path = os.path.join(DATA_DIR, f"{name}.csv")
        df.to_csv(save_path)
        success.append(name)
        print(f"[✓] {name:<12} — {len(df)} rows saved to {save_path}")

    except ValueError as e:
        failed.append(name)
        print(f"[✗] {name:<12} — {e}")

    except Exception as e:
        failed.append(name)
        print(f"[✗] {name:<12} — Unexpected error: {e}")

print(f"\nDone. {len(success)}/{len(STOCKS)} stocks downloaded successfully.")
if failed:
    print(f"Failed: {', '.join(failed)}")