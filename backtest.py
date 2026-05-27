import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date,timedelta
from strategy_sma import signals

def run_backtest(df,signals,initial_capital=100000):

    df = df.copy()

    df["Action"] = "HOLD AND DO NOT ENGAGE IN ANY TRADES"
    df["Price"] = df["Close"]
    df["Shares"] = 0.0
    df["Cash"] = float(initial_capital)
    df["Portfolio"] = float(initial_capital)
    df["Adjusted Portfolio"] = float(initial_capital)
    
    cash = float(initial_capital)
    shares = 0.0
    adjusted_cash = float(initial_capital)
    adjusted_shares = 0.0
    for i in range(len(df)):

        signal = signals.iloc[i]
        price = df["Price"].iloc[i]

        # BUY
        if signal == 1 and shares == 0:
            shares = cash/price
            adjusted_shares = cash / (price*1.001)
            cash = 0.0
            adjusted_cash = 0.0
            df.iloc[i, df.columns.get_loc("Action")] = "BUY THE SHARES AT CLOSE PRICE"

        # SELL
        elif signal == -1 and shares > 0:
            cash = shares*price
            adjusted_cash = adjusted_shares * price - 0.001*shares*price
            shares = 0.0
            adjusted_shares = 0.0
            df.iloc[i, df.columns.get_loc("Action")] = "SELL THE SHARES AT CLOSE PRICE"

        # UPDATE VALUES
        df.iloc[i, df.columns.get_loc("Shares")] = shares
        df.iloc[i, df.columns.get_loc("Cash")] = cash
        df.iloc[i, df.columns.get_loc("Portfolio")] = cash + shares * price
        df.iloc[i,df.columns.get_loc("Adjusted Portfolio")] = adjusted_cash+adjusted_shares*price
    return df

reliance = pd.read_csv("C:\\Users\\DELL\\OneDrive\\Desktop\\finpulse-lite\\data\\RELIANCE.csv")
reliance["Date"] = pd.to_datetime(reliance["Date"])
reliance = reliance.set_index("Date")
backtest = run_backtest(reliance,signals,100000)
final_portfolio = backtest["Portfolio"].iloc[-1]
adjusted_final_portfolio = backtest["Adjusted Portfolio"].iloc[-1]
if __name__=="_backtest_":
    print(f"Final Portfolio Value: ₹{final_portfolio:,.2f}")
    print(f"Adjusted Final Portfolio Value: ₹{adjusted_final_portfolio:,.2f}")
    # print(f"The difference is ₹{final_portfolio-adjusted_final_portfolio:,.2f}")

    shares = 100000/reliance["Close"].loc[reliance.index[reliance.index >= reliance.index[-1] - pd.DateOffset(years=5)][0]]
    reliance["Buy & Hold"] = reliance["Close"]*shares
    fig,ax1 = plt.subplots()
    ax1.plot(backtest.index,backtest["Adjusted Portfolio"],color="b")
    ax1.set_xlabel("Date",color="k")
    ax1.set_ylabel("Adjusted Portfolio",color="b")
    ax1.tick_params(axis="y",labelcolor="b")
    ax1.set_title("Reliance Equity Curve",color="green")
    ax2 = ax1.twinx()
    ax2.plot(reliance.index,reliance["Buy & Hold"],color="r")
    ax2.set_ylabel("Buy & Hold",color="r")
    ax2.tick_params(axis="y",labelcolor="r")
    fig.tight_layout()
    fig.savefig("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\images\RELIANCE_backtest.png")
    plt.show()
