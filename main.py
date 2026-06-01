import os
import pandas as pd
from .src.data_loader import load_data,DATA_DIR,STOCKS,get_stock_name
from .src.strategies import generate_signals
from .src.backtester import run_backtest
from .src.metrics import build_trade_log,trade_statistics
from .src.reporting import strategy_report


def run_full_pipeline(symbol, strategy_name="SMA"):
    name = get_stock_name(symbol)
    if name is None:
        raise KeyError(f"Unknown symbol: {symbol}")

    load_data(symbol)
    csv_path = os.path.join(DATA_DIR, f"{name}.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)

    df = pd.read_csv(csv_path, index_col="Date", parse_dates=True)

    signals = generate_signals(symbol, strategy_name)
    
    backtest = run_backtest(df, signals, initial_capital=100000)
    equity_curve = backtest["Adjusted Portfolio"]

    trade_log = build_trade_log(backtest)

    strategy_report(equity_curve, trade_log, symbol)


if __name__ == "__main__":
    try:
        symbol = input("Enter symbol: ").strip().upper()
        run_full_pipeline(symbol, strategy_name="SMA")

    except Exception as e:
        print(f"[✗] {type(e).__name__}: {e}")
