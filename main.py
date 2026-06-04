import os
import pandas as pd
from src.data_loader import load_data,DATA_DIR,STOCKS,get_stock_name
from src.strategies import generate_signals,generate_rsi_signals
from src.backtester import run_backtest
from src.metrics import build_trade_log,trade_statistics,total_return,sharpe_ratio
from src.reporting import strategy_report


def run_full_pipeline(symbol, strategy_name):
    name = get_stock_name(symbol)
    if name is None:
        raise KeyError(f"Unknown symbol: {symbol}")

    load_data(symbol)
    csv_path = os.path.join(DATA_DIR, f"{name}.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)

    df = pd.read_csv(csv_path, index_col="Date", parse_dates=True)
    if strategy_name == "SMA":
        signals = generate_signals(symbol, strategy_name)
    if strategy_name == "RSI":
        signals = generate_rsi_signals(symbol)

    backtest = run_backtest(df, signals, initial_capital=100000)
    equity_curve = backtest["Adjusted Portfolio"]

    trade_log = build_trade_log(backtest)

    strategy_report(equity_curve, trade_log, symbol,strategy_name)


if __name__ == "__main__":
    try:
        # symbol = input("Enter symbol: ").strip().upper()
        # strategy_name = input("Enter the strategy to be used: ").strip().upper()
        # run_full_pipeline(symbol, strategy_name)
        import csv

        results = []
        for name, symbol in STOCKS.items():
            try:
                load_data(symbol)
                sma_signals = generate_signals(symbol, strategy_name="SMA")
                rsi_signals = generate_rsi_signals(symbol)
                df          = pd.read_csv(os.path.join(DATA_DIR, f"{name}.csv"),
                                        index_col="Date", parse_dates=True)

                sma_bt   = run_backtest(df, sma_signals)
                rsi_bt   = run_backtest(df, rsi_signals)

                results.append({
                    "Stock":          symbol,
                    "SMA Return (%)": round(total_return(sma_bt["Adjusted Portfolio"]) * 100, 2),
                    "SMA Sharpe":     round(sharpe_ratio(sma_bt["Adjusted Portfolio"]), 2),
                    "RSI Return (%)": round(total_return(rsi_bt["Adjusted Portfolio"]) * 100, 2),
                    "RSI Sharpe":     round(sharpe_ratio(rsi_bt["Adjusted Portfolio"]), 2),
                })
            except Exception as e:
                print(f"[✗] {symbol} — {e}")

        df_summary = pd.DataFrame(results)
        df_summary.to_markdown("reports/summary.md", index=False)
        print("[✓] Summary table saved to reports/summary.md")

    except Exception as e:
        print(f"[✗] {type(e).__name__}: {e}")
