import pandas as pd
import numpy as np
from datetime import date,timedelta

def run_backtest(df,signals,initial_capital=100000):

    df = df.copy()

    df["Action"] = "HOLD AND DO NOT ENGAGE IN ANY TRADES"
    df["Price"] = df["Close"]
    df["Shares"] = 0.0
    df["Cash"] = float(initial_capital)
    df["Portfolio"] = float(initial_capital)

    cash = float(initial_capital)
    shares = 0.0

    for i in range(len(df)):

        signal = signals.iloc[i]
        price = df["Price"].iloc[i]

        # BUY
        if signal == 1 and shares == 0:

            shares = cash / price
            cash = 0.0

            df.iloc[i, df.columns.get_loc("Action")] = "BUY THE SHARES AT CLOSE PRICE"

        # SELL
        elif signal == -1 and shares > 0:

            cash = shares * price
            shares = 0.0

            df.iloc[i, df.columns.get_loc("Action")] = "SELL THE SHARES AT CLOSE PRICE"

        # UPDATE VALUES
        df.iloc[i, df.columns.get_loc("Shares")] = shares
        df.iloc[i, df.columns.get_loc("Cash")] = cash
        df.iloc[i, df.columns.get_loc("Portfolio")] = cash + shares * price

    return df

reliance = pd.read_csv("C:\\Users\\DELL\\OneDrive\\Desktop\\finpulse-lite\\data\\RELIANCE.csv")

reliance["Date"] = pd.to_datetime(reliance["Date"])
reliance = reliance.set_index("Date")

fiftydayMA = reliance["Close"].rolling(window=50).mean()
twohundreddayMA = reliance["Close"].rolling(window=200).mean()

signals = pd.Series(data=0,index=reliance.index)

signals.loc[fiftydayMA > twohundreddayMA] = 1
signals.loc[fiftydayMA < twohundreddayMA] = -1

signals = signals.shift(1).fillna(0)

backtest = run_backtest(reliance,signals,100000)

final_portfolio = backtest["Portfolio"].iloc[-1]

print(f"Final Portfolio Value: ₹{final_portfolio:,.2f}")