import os
import numpy as np
import pandas as pd
from .data_loader import STOCKS,get_stock_name

def total_return(equity_curve):
    return equity_curve.iloc[-1] / equity_curve.iloc[0] - 1

def annualized_return(equity_curve):
    years = (equity_curve.index[-1] - equity_curve.index[0]).days / 365
    return (equity_curve.iloc[-1] / equity_curve.iloc[0]) ** (1 / years) - 1

def max_drawdown(equity_curve):
    peak = equity_curve.cummax()
    drawdown = equity_curve / peak - 1
    return drawdown.min()

def sharpe_ratio(equity_curve, risk_free_rate=0.065):
    returns = equity_curve.pct_change().dropna()
    annual_mean = returns.mean() * 252
    annual_std = returns.std() * np.sqrt(252)
    return (annual_mean - risk_free_rate) / annual_std

def build_trade_log(backtest):

    trades = []

    buy_date = None
    buy_price = None
    buy_shares = None

    for i in range(len(backtest)):
        action = backtest["Action"].iloc[i]

        if action == "BUY":
            buy_date = backtest.index[i]
            buy_price = backtest["Price"].iloc[i]
            buy_shares = backtest["Shares"].iloc[i]

        elif action == "SELL" and buy_price is not None:
            sell_price = backtest["Price"].iloc[i]

            profit = ((sell_price * 0.999) - (buy_price * 1.001)) * buy_shares

            trades.append(
                {
                    "Buy Date": buy_date,
                    "Sell Date": backtest.index[i],
                    "Buy Price": round(buy_price, 2),
                    "Sell Price": round(sell_price, 2),
                    "Shares": round(buy_shares, 4),
                    "Profit": round(profit, 2),
                }
            )

            buy_date = None
            buy_price = None
            buy_shares = None

    return pd.DataFrame(trades)

def trade_statistics(trade_log):

    if trade_log.empty:
        return {"num_trades": 0, "win_rate": 0, "profit_factor": 0}

    wins = trade_log[trade_log["Profit"] > 0]

    losses = trade_log[trade_log["Profit"] < 0]

    win_rate = len(wins) / len(trade_log)

    loss_sum = losses["Profit"].sum()

    profit_factor = (wins["Profit"].sum() / abs(loss_sum) if loss_sum != 0 else float("inf"))

    return {"num_trades": len(trade_log), "win_rate": win_rate, "profit_factor": profit_factor}


if __name__ == "__main__":

    import pandas as pd
    from .strategies import generate_signals,generate_rsi_signals
    from .backtester import run_backtest
    from .data_loader import DATA_DIR

    try:
        symbol = input("Enter symbol: ").strip().upper()
        strategy_name = input("Enter the strategy to be used: ").strip().upper()
        name = get_stock_name(symbol)

        if name is None:
            raise KeyError(f"Unknown symbol: {symbol}")

        df = pd.read_csv(
            os.path.join(DATA_DIR, f"{name}.csv"),
            index_col="Date",
            parse_dates=True
        )

        if strategy_name == "SMA":
            signals = generate_signals(symbol)
        elif strategy_name == "RSI":
            signals = generate_rsi_signals(symbol,14,30,70)

        backtest = run_backtest(df, signals)

        equity_curve = backtest["Adjusted Portfolio"]

        trade_log = build_trade_log(backtest)

        # ✅ FIXED: Now actually prints the metrics instead of just calculating them
        print("\n" + "="*50)
        print(f"PERFORMANCE METRICS FOR {name} using {strategy_name} STRATEGY")
        print("="*50)
        print(f"Total Return: {total_return(equity_curve)*100:.2f}%")
        print(f"Annualized Return: {annualized_return(equity_curve)*100:.2f}%")
        print(f"Sharpe Ratio: {sharpe_ratio(equity_curve):.2f}")
        print(f"Max Drawdown: {max_drawdown(equity_curve)*100:.2f}%")
        
        stats = trade_statistics(trade_log)
        print(f"\nNumber of Trades: {stats['num_trades']}")
        print(f"Win Rate: {stats['win_rate']*100:.2f}%")
        print(f"Profit Factor: {stats['profit_factor']:.2f}")
        
        if not trade_log.empty:
            print(f"\nTotal Profit: ₹ {trade_log['Profit'].sum():.2f}")
            print("\nTrade Log:")
            print(trade_log)
        print("="*50 + "\n")

    except Exception as e:
        print(f"[✗] {type(e).__name__}: {e}")
