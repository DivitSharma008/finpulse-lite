import pandas as pd 
from datetime import date,timedelta
import matplotlib.pyplot as plt

stocks =["RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","ITC","SBIN","LT","HINDUNILVR","KOTAKBANK"]

base_path = r"C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data"

def plot_MA(stock):
    df = pd.read_csv(fr"{base_path}\{stock}.csv",usecols=["Close","Date"])
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")
    plt.plot(df,label = "Closing Price")
    plt.plot(df["Close"].rolling(window=50).mean(),label = "50 Day Moving Average")
    plt.plot(df["Close"].rolling(window=200).mean(),label="200 Day Moving Average")
    plt.xlim(left=date.today()-timedelta(days=365*5),right = date.today())
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"Moving Averages-{stock}")
    plt.legend()
    plt.show()

for stock in stocks:
    plot_MA(stock)