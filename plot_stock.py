import pandas as pd
import matplotlib.pyplot as plt
import os

STOCKS     = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "ITC", "SBIN", "LT", "HINDUNILVR", "KOTAKBANK"]
DATA_DIR   = r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\data"
IMAGES_DIR = r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\images"

os.makedirs(IMAGES_DIR, exist_ok=True)

def plot_MA(stock):
    path = os.path.join(DATA_DIR, f"{stock}.csv")
    try:
        df = pd.read_csv(path, usecols=["Date", "Close"])
        df["Date"] = pd.to_datetime(df["Date"], utc=True)
        df["Date"] = df["Date"].dt.tz_localize(None)
        df = df.set_index("Date")

        df["50 MA"]  = df["Close"].rolling(window=50).mean()
        df["200 MA"] = df["Close"].rolling(window=200).mean()

        plt.figure(figsize=(13, 5))
        plt.plot(df.index, df["Close"],  label="Closing Price")
        plt.plot(df.index, df["50 MA"],  label="50 Day Moving Average")
        plt.plot(df.index, df["200 MA"], label="200 Day Moving Average")
        plt.xlabel("Date")
        plt.ylabel("Price (₹)")
        plt.title(f"Moving Averages — {stock}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGES_DIR, f"{stock}_chart.png"))
        plt.show()
        plt.close()  # free memory

    except FileNotFoundError:
        print(f"[✗] {stock:<12} — CSV not found at {path}. Run download_data.py first.")
    except Exception as e:
        print(f"[✗] {stock:<12} — Error: {e}")

for stock in STOCKS:
    plot_MA(stock)