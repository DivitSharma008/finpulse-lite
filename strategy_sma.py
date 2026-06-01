import pandas as pd
import os

from download_data import STOCKS, DATA_DIR,get_stock_name

SUPPORTED_STRATEGIES = ["SMA"]

def generate_signals(symbol, strategy_name="SMA"):
    name = get_stock_name(symbol)

    if name is None:
        raise KeyError(f"Unknown symbol: {symbol}")

    if strategy_name not in SUPPORTED_STRATEGIES:
        raise ValueError(
            f"Unsupported strategy. Supported: {SUPPORTED_STRATEGIES}"
        )

    path = os.path.join(DATA_DIR, f"{name}.csv")

    df = pd.read_csv(path)

    if len(df) < 200:
        raise ValueError(
            "Not enough data to calculate 200-day SMA."
        )

    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    sma50 = df["Close"].rolling(50).mean()
    sma200 = df["Close"].rolling(200).mean()

    signals = pd.Series(0, index=df.index)

    signals.loc[sma50 > sma200] = 1
    signals.loc[sma50 < sma200] = -1

    signals = signals.shift(1).fillna(0)
    print("[✓] Signals generated")
    return signals

if __name__ == "__main__":

    symbol = input("Enter symbol: ").strip().upper()

    try:
        signals = generate_signals(symbol)
        print(signals.value_counts())

    except Exception as e:
        print(f"[✗] {e}")