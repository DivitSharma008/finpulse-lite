import pandas as pd
import yfinance as yf
import os
from datetime import date, timedelta

STOCKS = {
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "INFY": "INFY.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "SBIN": "SBIN.NS",
    "ITC": "ITC.NS",
    "LT": "LT.NS",
    "HINDUNILVR": "HINDUNILVR.NS",
    "KOTAKBANK": "KOTAKBANK.NS",
}

DATA_DIR = r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\data"

START = date.today() - timedelta(days=5 * 365)
END = date.today()

os.makedirs(DATA_DIR, exist_ok=True)

def get_stock_name(symbol):
    inverted_dict = {v: k for k, v in STOCKS.items()}
    return inverted_dict.get(symbol)

def load_data(symbol):
    inverted_dict = {v: k for k, v in STOCKS.items()}
    name = inverted_dict.get(symbol)

    if name is None:
        raise KeyError(f"'{symbol}' not found. Valid symbols: {', '.join(STOCKS.values())}")

    ticker = yf.Ticker(symbol)
    df = ticker.history(start=START, end=END)

    if df.empty:
        raise ValueError(f"No data returned for '{symbol}'")

    df.index = pd.to_datetime(df.index.date)
    df.index.name = "Date"

    save_path = os.path.join(DATA_DIR, f"{name}.csv")
    df.to_csv(save_path)

    print(f"[✓] {name} — {len(df)} rows saved")

    return save_path

if __name__ == "__main__":
    try:
        symbol = input("Enter symbol: ").strip().upper()
        load_data(symbol)

    except Exception as e:
        print(f"[✗] {type(e).__name__}: {e}")
