import pandas as pd
import os
from .data_loader import STOCKS, DATA_DIR, get_stock_name
SUPPORTED_STRATEGIES = ["SMA", "RSI"]


def generate_signals(symbol, strategy_name="SMA"):
    name = get_stock_name(symbol)

    if name is None:
        raise KeyError(f"Unknown symbol: {symbol}")

    if strategy_name not in SUPPORTED_STRATEGIES:
        raise ValueError(f"Unsupported strategy. Supported: {SUPPORTED_STRATEGIES}")

    csv_path = os.path.join(DATA_DIR, f"{name}.csv")

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Data file not found: {csv_path}\n"
            f"Run: python -m data_loader and enter symbol {name}"
        )

    df = pd.read_csv(csv_path, index_col="Date", parse_dates=True)
    if len(df) < 200:
        raise ValueError("Not enough data to calculate 200-day SMA.")

    sma50 = df["Close"].rolling(50).mean()
    sma200 = df["Close"].rolling(200).mean()

    signals = pd.Series(0, index=df.index)
    signals.loc[sma50 > sma200] = 1
    signals.loc[sma50 < sma200] = -1
    signals = signals.shift(1).fillna(0)

    print("[✓] SMA Signals generated")
    return signals


def generate_rsi_signals(symbol, period=14, oversold=30, overbought=70,strategy_name="RSI"):
    name = get_stock_name(symbol)

    if name is None:
        raise KeyError(f"Unknown symbol: {symbol}")

    path = os.path.join(DATA_DIR, f"{name}.csv")
    df = pd.read_csv(path, index_col="Date", parse_dates=True)

    if len(df) < period:
        raise ValueError(f"Not enough data to calculate RSI with period={period}.")

    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = delta.clip(upper=0).abs()

    avg_gain = gain.ewm(span = period, adjust=False).mean()
    avg_loss = loss.ewm(span = period, adjust=False).mean()

    RS = avg_gain / avg_loss.replace(0,1e-10)
    RSI = 100 - 100 / (1 + RS)

    signals = pd.Series(0, index=df.index)
    signals.loc[RSI < oversold] = 1
    signals.loc[RSI > overbought] = -1
    signals = signals.shift(1).fillna(0)
    signals.iloc[:30] = 0  # Ignore unreliable early signals
    print("[✓] RSI Signals generated")
    return signals

if __name__ == "__main__":
    symbol = input("Enter symbol: ").strip().upper()
    strategy_name = input("Enter the strategy to be used: ").strip().upper()
    try:
        if strategy_name == "SMA":
            signals = generate_signals(symbol)
        elif strategy_name == "RSI":
            signals = generate_rsi_signals(symbol,14,30,70)
        print(signals.value_counts())

    except Exception as e:
        print(f"[✗] {e}")
