try:
    from .metrics import (
        total_return,
        annualized_return,
        sharpe_ratio,
        max_drawdown,
        build_trade_log,
        trade_statistics,
    )
    from .data_loader import STOCKS,get_stock_name,BASE_DIR
except ImportError:
    from metrics import (
        total_return,
        annualized_return,
        sharpe_ratio,
        max_drawdown,
        build_trade_log,
        trade_statistics,
    )
    from data_loader import STOCKS,get_stock_name,BASE_DIR
import os

def strategy_report(equity_curve, trade_log, symbol,strategy_name):
    stats = trade_statistics(trade_log)
    name = get_stock_name(symbol)
    content = f"""
# Backtest Report

Strategy         : {strategy_name} STRATEGY
Stock            : {symbol}
Period           : {equity_curve.index[0].date()} -> {equity_curve.index[-1].date()}
________________________________________________
Total Return     : {total_return(equity_curve) * 100:.2f}%
Annualized Return: {annualized_return(equity_curve) * 100:.2f}%
Sharpe Ratio     : {sharpe_ratio(equity_curve):.2f}
Max Drawdown     : {max_drawdown(equity_curve) * 100:.2f}%
Win Rate         : {stats["win_rate"] * 100:.2f}%
Number of Trades : {stats["num_trades"]}
________________________________________________
"""
    REPORT_DIR = os.path.join(BASE_DIR, "reports")
    os.makedirs(REPORT_DIR, exist_ok=True)
    path = os.path.join(REPORT_DIR, f"{name}_{strategy_name}_report.md")
    with open(path, "w") as f:
        f.write(content)
    print(f"[✓] Report saved: {path}")

if __name__ == "__main__":
    try:
        import pandas as pd
        from .strategies import generate_signals,generate_rsi_signals
        from .backtester import run_backtest
        from .data_loader import DATA_DIR,BASE_DIR
    except:
        import pandas as pd
        from strategies import generate_signals,generate_rsi_signals
        from backtester import run_backtest
        from data_loader import DATA_DIR,BASE_DIR

    try:
        symbol = input("Enter symbol: ").strip().upper()
        strategy_name = input("Enter the strategy to be used: ").strip().upper()
        name = get_stock_name(symbol)

        if name is None:
            raise KeyError(f"Unknown symbol: {symbol}")

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

        equity_curve = backtest["Adjusted Portfolio"]

        trade_log = build_trade_log(backtest)

        strategy_report(
            equity_curve,
            trade_log,
            symbol,strategy_name
        )

    except Exception as e:
        print(f"[✗] {type(e).__name__}: {e}")
