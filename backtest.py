import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from strategy_sma import signals

def run_backtest(df, signals, initial_capital=100000):
    df = df.copy()

    df["Action"]             = "HOLD"
    df["Price"]              = df["Close"]
    df["Shares"]             = 0.0
    df["Cash"]               = float(initial_capital)
    df["Portfolio"]          = float(initial_capital)
    df["Adjusted Portfolio"] = float(initial_capital)

    cash            = float(initial_capital)
    shares          = 0.0
    adjusted_cash   = float(initial_capital)
    adjusted_shares = 0.0

    for i in range(len(df)):
        signal = signals.iloc[i]
        price  = df["Price"].iloc[i]

        # BUY
        if signal == 1 and shares == 0:
            shares          = cash / price
            adjusted_shares = cash / (price * 1.001)   # 0.1% slippage on buy
            cash = adjusted_cash = 0.0
            df.iloc[i, df.columns.get_loc("Action")] = "BUY"

        # SELL
        elif signal == -1 and shares > 0:
            cash          = shares * price
            adjusted_cash = adjusted_shares * price - 0.001 * shares * price  # 0.1% cost on sell
            shares = adjusted_shares = 0.0
            df.iloc[i, df.columns.get_loc("Action")] = "SELL"

        # UPDATE
        df.iloc[i, df.columns.get_loc("Shares")]            = shares
        df.iloc[i, df.columns.get_loc("Cash")]              = cash
        df.iloc[i, df.columns.get_loc("Portfolio")]         = cash + shares * price
        df.iloc[i, df.columns.get_loc("Adjusted Portfolio")]= adjusted_cash + adjusted_shares * price

    return df


# ── Load Data ─────────────────────────────────────────────────────────────────
reliance = pd.read_csv(r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\data\RELIANCE.csv")
reliance["Date"] = pd.to_datetime(reliance["Date"])
reliance = reliance.set_index("Date")

# ── Run Backtest ──────────────────────────────────────────────────────────────
backtest = run_backtest(reliance, signals, 100000)

final_portfolio          = backtest["Portfolio"].iloc[-1]
adjusted_final_portfolio = backtest["Adjusted Portfolio"].iloc[-1]

if __name__ == "__main__":
    print(f"Final Portfolio Value:          ₹{final_portfolio:,.2f}")
    print(f"Adjusted Final Portfolio Value: ₹{adjusted_final_portfolio:,.2f}")

    # Buy & Hold — invest ₹1,00,000 at the very first price
    reliance["Buy & Hold"] = reliance["Close"] * (100000 / reliance["Close"].iloc[0])

    # Single Y-axis so both lines are directly comparable
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(backtest.index, backtest["Adjusted Portfolio"], color="b", label="Strategy (adj.)")
    ax.plot(reliance.index, reliance["Buy & Hold"],         color="r", label="Buy & Hold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value (₹)")
    ax.set_title("Reliance Equity Curve", color="green")
    ax.legend()
    fig.tight_layout()
    fig.savefig(r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\images\RELIANCE_backtest.png")
    plt.show()



    
