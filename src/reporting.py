from metrics import total_return,annualized_return,sharpe_ratio,max_drawdown,build_trade_log,trade_statistics,trade_log,STOCKS
import os

def strategy_report(equity_curve, trade_log, symbol):
    stats = trade_statistics(trade_log)
    inverted_dict = {v: k for k, v in STOCKS.items()}
    name = inverted_dict.get(symbol, symbol)
    content = f"""
# Backtest Report

Strategy         : SMA Crossover (50/200)
Stock            : {symbol}
Period           : {equity_curve.index[0]} -> {equity_curve.index[-1]}
________________________________________________
Total Return     : {total_return(equity_curve) * 100:.2f}%
Annualized Return: {annualized_return(equity_curve) * 100:.2f}%
Sharpe Ratio     : {sharpe_ratio(equity_curve):.2f}
Max Drawdown     : {max_drawdown(equity_curve) * 100:.2f}%
Win Rate         : {stats["win_rate"] * 100:.2f}%
Number of Trades : {stats["num_trades"]}
________________________________________________
"""

    report_dir = (r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\reports")
    os.makedirs(report_dir, exist_ok=True)
    path = os.path.join(report_dir, f"{name}_SMA_report.md")
    with open(path, "w") as f:
        f.write(content)
    print(f"[✓] Report saved: {path}")

if __name__ == "__main__":

    import pandas as pd
    from strategies import generate_signals
    from backtester import run_backtest
    from data_loader import DATA_DIR

    try:
        symbol = input("Enter symbol: ").strip().upper()

        inverted_dict = {v: k for k, v in STOCKS.items()}
        name = inverted_dict.get(symbol)

        if name is None:
            raise KeyError(f"Unknown symbol: {symbol}")

        df = pd.read_csv(
            os.path.join(DATA_DIR, f"{name}.csv"),
            index_col="Date",
            parse_dates=True
        )

        signals = generate_signals(symbol)

        backtest = run_backtest(df, signals)

        equity_curve = backtest["Adjusted Portfolio"]

        trade_log = build_trade_log(backtest)

        strategy_report(
            equity_curve,
            trade_log,
            symbol
        )

    except Exception as e:
        print(f"[✗] {type(e).__name__}: {e}")