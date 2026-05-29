import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from backtest import backtest, signals

equity_curve = backtest["Adjusted Portfolio"]

# ── Return Metrics ────────────────────────────────────────────────────────────
def total_return(equity_curve):
    return equity_curve.iloc[-1] / equity_curve.iloc[0] - 1

def annualized_return(equity_curve):
    years = (equity_curve.index[-1] - equity_curve.index[0]).days / 365
    return (equity_curve.iloc[-1] / equity_curve.iloc[0]) ** (1 / years) - 1

print(f"Total Return     : {round(total_return(equity_curve) * 100, 2)}%")
print(f"Annualized Return: {round(annualized_return(equity_curve) * 100, 2)}%")

# ── Drawdown ──────────────────────────────────────────────────────────────────
def max_drawdown(equity_curve):
    peak     = equity_curve.cummax()
    drawdown = equity_curve / peak - 1
    max_dd   = drawdown.min()
    dd_start = equity_curve.loc[:drawdown.idxmin()].idxmax()
    dd_end   = drawdown.idxmin()
    return max_dd, dd_start, dd_end, drawdown

max_dd, dd_start, dd_end, drawdown = max_drawdown(equity_curve)
print(f"Max Drawdown     : {round(max_dd * 100, 2)}%")
print(f"DD Period        : {dd_start.date()} → {dd_end.date()}")

plt.figure()
plt.plot(drawdown)
plt.fill_between(drawdown.index, drawdown.values, 0, alpha=0.3, color="red")
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.title("Daily Drawdown")
plt.tight_layout()
plt.show()

# ── Sharpe Ratio ──────────────────────────────────────────────────────────────
def sharpe_ratio(equity_curve, risk_free_rate=0.065):
    daily_return      = equity_curve.pct_change().dropna()
    annual_mean       = daily_return.mean() * 252
    annual_std        = daily_return.std() * np.sqrt(252)
    return (annual_mean - risk_free_rate) / annual_std

sharpe = round(sharpe_ratio(equity_curve), 2)
print(f"Sharpe Ratio     : {sharpe}")

# ── Trade Log ─────────────────────────────────────────────────────────────────
trade_log = []
buy_date = buy_price = buy_shares = None

for i in range(len(backtest)):
    action = backtest["Action"].iloc[i]

    if action == "BUY":
        buy_date   = backtest.index[i]
        buy_price  = backtest["Price"].iloc[i]
        buy_shares = backtest["Shares"].iloc[i]

    elif action == "SELL" and buy_price is not None:
        sell_date  = backtest.index[i]
        sell_price = backtest["Price"].iloc[i]
        profit     = (sell_price * 0.999 - buy_price * 1.001) * buy_shares
        trade_log.append({
            "Buy Date":   buy_date,
            "Sell Date":  sell_date,
            "Buy Price":  round(buy_price, 2),
            "Sell Price": round(sell_price, 2),
            "Shares":     round(buy_shares, 4),
            "Profit":     round(profit, 2),
        })
        buy_date = buy_price = buy_shares = None   # reset

trade_log = pd.DataFrame(trade_log)
print("\nTrade Log:")
print(trade_log.to_string(index=False))

# ── Trade Statistics ──────────────────────────────────────────────────────────
def trade_statistics(trade_log):
    if trade_log.empty:
        print("No completed trades.")
        return

    n          = len(trade_log)
    wins       = trade_log[trade_log["Profit"] > 0]
    losses     = trade_log[trade_log["Profit"] < 0]
    winrate    = len(wins) / n
    avg_win    = wins["Profit"].mean()   if not wins.empty   else 0
    avg_loss   = losses["Profit"].mean() if not losses.empty else 0
    loss_sum   = losses["Profit"].sum()
    pf         = wins["Profit"].sum() / abs(loss_sum) if loss_sum != 0 else float("inf")

    print(f"\nNumber of Trades : {n}")
    print(f"Win Rate         : {round(winrate * 100, 2)}%")
    print(f"Avg Win (₹)      : ₹{avg_win:,.2f}")
    print(f"Avg Loss (₹)     : ₹{avg_loss:,.2f}")
    print(f"Profit Factor    : {round(pf, 2)}")

trade_statistics(trade_log)

# ── Strategy Report ───────────────────────────────────────────────────────────
def strategy_report(equity_curve, trade_log):
    content = f"""
# Backtest Report

    Strategy         : SMA Crossover (50/200)
    Stock            : RELIANCE.NS
    Period           : {equity_curve.index[0].date()} to {equity_curve.index[-1].date()}
    _____________________________________________
    Total Return     : {round(total_return(equity_curve) * 100, 2)}%
    Annualized Return: {round(annualized_return(equity_curve) * 100, 2)}%
    Sharpe Ratio     : {sharpe}
    Max Drawdown     : {round(max_dd * 100, 2)}%
    Number of Trades : {len(trade_log)}
    Win Rate         : {round(len(trade_log[trade_log['Profit'] > 0]) / len(trade_log) * 100, 2) if not trade_log.empty else 'N/A'}%
    _____________________________________________
"""
    with open(r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\reports\RELIANCE_SMA_report.md", "w") as f:
        f.write(content)
    print("\nReport saved.")

strategy_report(equity_curve, trade_log)
