import pandas as pd
import numpy as np
from datetime import date,timedelta

def run_backtest(df,signals,initial_capital=100000):
    df = df.assign(Action="HOLD AND DO NOT ENGAGE IN ANY TRADES", Price=df["Close"], Shares=np.nan, Cash=np.nan, Portfolio=float(initial_capital))
    
    trade_trigger = signals.diff().fillna(signals)
    buys = trade_trigger == 1
    sells = trade_trigger < 0
    
    df["Available Cash"] = float(initial_capital)
    
    df.loc[buys,"Action"] = "BUY THE SHARES AT CLOSE PRICE"
    df.loc[buys,"Shares"] = df["Available Cash"]/df["Price"]
    df.loc[buys,"Cash"] = 0.0
    
    df["Buy Price"] = np.nan
    df.loc[buys,"Buy Price"] = df["Price"]

    df.loc[sells,"Action"] = "SELL THE SHARES AT CLOSE PRICE"
    df.loc[sells,"Shares"] = 0.0
    df.loc[sells, "Cash"] = (df["Available Cash"].ffill() / df["Buy Price"].ffill()) * df["Price"]

    df.loc[trade_trigger == 1, "Cash"] = 0.0
    df.loc[trade_trigger <= 0, "Shares"] = 0.0

    df["Shares"] = df.Shares.ffill().fillna(0)
    df["Cash"] = df.Cash.ffill().fillna(initial_capital)
    
    df.loc[signals <= 0, "Available Cash"] = df["Cash"]
    df["Available Cash"] = df["Available Cash"].ffill().fillna(initial_capital)
    
    df["Portfolio"] = df["Cash"]+df["Shares"]*df["Price"]

    df = df.drop(columns = ["Buy Price", "Available Cash"])
    return df

reliance = pd.read_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\RELIANCE.csv")
reliance["Date"] = pd.to_datetime(reliance["Date"])
reliance = reliance.set_index("Date")
fiftydayMA = reliance["Close"].rolling(window="50D").mean()
twohundreddayMA = reliance["Close"].rolling(window="200D").mean()
signals = pd.Series(data=0,index=reliance.index)
signals.loc[fiftydayMA<twohundreddayMA] = -1
signals.loc[fiftydayMA>twohundreddayMA] = 1    
signals = signals.shift(1).fillna(0)
backtest = run_backtest(reliance,signals,100000)

final_portfolio = backtest["Portfolio"].iloc[-1]
print(f"Final Portfolio Value: ₹{final_portfolio:,.2f}")
