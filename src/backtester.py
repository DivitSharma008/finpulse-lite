import pandas as pd
import matplotlib.pyplot as plt
import os

from strategies import generate_signals
from data_loader import DATA_DIR, STOCKS, get_stock_name


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

        if signal == 1 and shares <= 1e-10:
            shares = cash / price

            adjusted_shares = adjusted_cash / (price * 1.001)

            cash = 0.0
            adjusted_cash = 0.0

            df.iloc[i, df.columns.get_loc("Action")] = "BUY"

        elif signal == -1 and shares > 1e-10:
            cash = shares * price

            adjusted_cash = adjusted_shares * price * 0.999

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

    try:
        name = get_stock_name(symbol)

        df = pd.read_csv(os.path.join(DATA_DIR, f"{name}.csv"), index_col="Date", parse_dates=True)

        signals = generate_signals(symbol)

        backtest = run_backtest(df, signals)
       
        print("Final Portfolio: ₹", round(backtest["Adjusted Portfolio"].iloc[-1], 2))

        # ✅ FIXED: Removed duplicate line
        df["Buy & Hold"] = df["Close"] * (100000 / df["Close"].iloc[0])

        fig, ax = plt.subplots(figsize=(13, 5))

        ax.plot(
            backtest.index,
            backtest["Adjusted Portfolio"],
            color="b",
            label="Strategy (adj.)"
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

        # ✅ FIXED: Portable path using os.path.join()
        images_dir = os.path.join(r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite", "images")
        os.makedirs(images_dir, exist_ok=True)
        fig.savefig(os.path.join(images_dir, f"{name}_backtest.png"))

        plt.show()

    except Exception as e:
        print(f"[✗] {e}")
