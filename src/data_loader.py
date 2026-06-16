import pandas as pd
import yfinance as yf
import os
from datetime import date, timedelta

STOCKS = {
    "ADANIENSOL": "ADANIENSOL.NS",
    "ADANIGREEN": "ADANIGREEN.NS",
    "ADANIPORTS": "ADANIPORTS.NS",
    "APOLLOHOSP": "APOLLOHOSP.NS",
    "ASIANPAINT": "ASIANPAINT.NS",
    "AXISBANK": "AXISBANK.NS",
    "BAJAJ-AUTO": "BAJAJ-AUTO.NS",
    "BAJAJFINSV": "BAJAJFINSV.NS",
    "BAJAJHLDNG": "BAJAJHLDNG.NS",
    "BHARATIARTL": "BHARATIARTL.NS",
    "BPCL": "BPCL.NS",
    "BRITANNIA": "BRITANNIA.NS",
    "CIPLA": "CIPLA.NS",
    "COALINDIA": "COALINDIA.NS",
    "DRREDDY": "DRREDDY.NS",
    "EICHERMOT": "EICHERMOT.NS",
    "GAIL": "GAIL.NS",
    "GRASIM": "GRASIM.NS",
    "HCLTECH": "HCLTECH.NS",
    "HDFC": "HDFC.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "HEROMOTOCO": "HEROMOTOCO.NS",
    "HINDUNILVR": "HINDUNILVR.NS",
    "HONEYWELL": "HONEYWELL.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "INFY": "INFY.NS",
    "ITC": "ITC.NS",
    "JSWSTEEL": "JSWSTEEL.NS",
    "KOTAKBANK": "KOTAKBANK.NS",
    "LT": "LT.NS",
    "MARUTI": "MARUTI.NS",
    "NESTLEIND": "NESTLEIND.NS",
    "NTPC": "NTPC.NS",
    "ONGC": "ONGC.NS",
    "POWERGRID": "POWERGRID.NS",
    "RELIANCE": "RELIANCE.NS",
    "SBIN": "SBIN.NS",
    "SBICARD": "SBICARD.NS",
    "SHREECEM": "SHREECEM.NS",
    "SUNPHARMA": "SUNPHARMA.NS",
    "TATAMOTORS": "TATAMOTORS.NS",
    "TATAPOWER": "TATAPOWER.NS",
    "TATASTEEL": "TATASTEEL.NS",
    "TCS": "TCS.NS",
    "TECHM": "TECHM.NS",
    "TITAN": "TITAN.NS",
    "ULTRACEMCO": "ULTRACEMCO.NS",
    "UPL": "UPL.NS",
    "WIPRO": "WIPRO.NS",
}
# Replace the hardcoded line with:
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


START = date.today() - timedelta(days=5 * 365)
END = date.today()

os.makedirs(DATA_DIR, exist_ok=True)

def get_stock_name(symbol):
    inverted_dict = {v: k for k, v in STOCKS.items()}
    return inverted_dict.get(symbol)

def load_data(symbol):
    name = get_stock_name(symbol)

    if name is None:
        raise KeyError(f"'{symbol}' not found. Valid symbols: {', '.join(STOCKS.keys())}")

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