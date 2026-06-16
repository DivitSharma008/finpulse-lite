import pandas as pd
import matplotlib.pyplot as plt
import os

from .strategies import generate_signals,generate_rsi_signals
from .data_loader import DATA_DIR, STOCKS, get_stock_name,BASE_DIR


def run_backtest(df, signals, initial_capital=100000):

    df = df.copy()

    df["Action"] = "HOLD"
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

        if signal == 1 and shares <= 1e-8:  #the shares condition forces no buys even after a repeated buy signal
            shares = cash / price
            transcation_cost = 0.001
            adjusted_shares = adjusted_cash / (price * (1+transcation_cost))

            cash = 0.0
            adjusted_cash = 0.0

            df.iloc[i, df.columns.get_loc("Action")] = "BUY"

        elif signal == -1 and shares > 1e-10:
            cash = shares * price

            adjusted_cash = adjusted_shares * price *(1-transcation_cost)

            shares = 0.0
            adjusted_shares = 0.0

            df.iloc[i, df.columns.get_loc("Action")] = "SELL"

        df.iloc[i, df.columns.get_loc("Shares")] = shares
        df.iloc[i, df.columns.get_loc("Cash")] = cash

        df.iloc[i, df.columns.get_loc("Portfolio")] = cash + shares * price

        df.iloc[i, df.columns.get_loc("Adjusted Portfolio")] = (adjusted_cash + adjusted_shares * price)
    print("[✓] Backtest completed")
    return df

if __name__ == "__main__":
    symbol = input("Enter symbol: ").strip().upper()
    strategy_name = input("Enter the strategy to be used: ").strip().upper()
    try:
        name = get_stock_name(symbol)

        csv_path = os.path.join(DATA_DIR, f"{name}.csv")

        if not os.path.exists(csv_path):
            raise FileNotFoundError(
                f"Data file not found: {csv_path}\n"
                f"Run: python -m data_loader and enter symbol {name}"
            )

        df = pd.read_csv(csv_path, index_col="Date", parse_dates=True)
        if strategy_name == "SMA":
            signals = generate_signals(symbol)
        elif strategy_name == "RSI":
            signals = generate_rsi_signals(symbol,14,30,70)
        backtest = run_backtest(df, signals)
       
        print("Final Portfolio: ₹", round(backtest["Adjusted Portfolio"].iloc[-1], 2))

        df["Buy & Hold"] = df["Close"] * (100000 / df["Close"].iloc[0])

        fig, ax = plt.subplots(figsize=(13, 5))

        ax.plot(
            backtest.index,
            backtest["Adjusted Portfolio"],
            color="b",
            label=f"{strategy_name} Strategy"
        )

        ax.plot(
            df.index,
            df["Buy & Hold"],
            color="r",
            label="Buy & Hold"
        )

        ax.set_xlabel("Date")
        ax.set_ylabel("Portfolio Value (₹)")
        ax.set_title(f"{name} Equity Curve", color="green")
        ax.legend()

        fig.tight_layout()

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        IMG_DIR = os.path.join(BASE_DIR, "images")
        os.makedirs(IMG_DIR, exist_ok=True)
        fig.savefig(os.path.join(IMG_DIR, f"{name}_backtest.png"))

        plt.show()

    except Exception as e:
        print(f"[✗] {e}")
