import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from datetime import date,timedelta
from backtest import backtest,signals

equity_curve = backtest["Adjusted Portfolio"]

def total_return(equity_curve):
    return (equity_curve.iloc[-1]/equity_curve.iloc[0]-1)

def annualized_return(equity_curve):
    years = (equity_curve.index[-1]-equity_curve.index[0]).days/365
    return(((equity_curve.iloc[-1]/equity_curve.iloc[0])**(1/years))-1)

print("The total return is",round(total_return(equity_curve)*100,2),"%")
print("The annualized return is",round(annualized_return(equity_curve)*100,2),"%")


def max_drawdown(equity_curve):
    maxtillnow = equity_curve.cummax()
    drawdown = equity_curve/maxtillnow-1
    maxi_drawdown = drawdown.min()
    return maxi_drawdown,equity_curve.loc[:drawdown.idxmin()].idxmax(),drawdown.idxmin(),drawdown

maxi_drawdown,start_date,end_date,drawdown=max_drawdown(equity_curve)
print("The maximum drawdown is ",round(maxi_drawdown*100,2),"%")
print("The starting and ending dates are ",start_date,"and",end_date)

plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.title("Daily Drawdown")
plt.plot(drawdown)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()

def sharpe_ratio(equity_curve,risk_free_rate=0.065):
    daily_return = equity_curve.pct_change().dropna()
    mean = daily_return.mean()
    std_deviation = daily_return.std()
    annual_mean = mean*252
    annual_std_deviation = std_deviation*np.sqrt(252)
    sharpe = (annual_mean-risk_free_rate)/annual_std_deviation
    return sharpe

sharpe = round(sharpe_ratio(equity_curve),2)
print("The Sharpe ratio for investment in Reliance is",sharpe)

trade_log = []
buy_date = np.nan
sell_date = np.nan
buy_shares = np.nan

for i in range(len(backtest)):
    action = backtest["Action"].iloc[i]
    if action == "BUY THE SHARES AT CLOSE PRICE":
        buy_date = backtest.index[i]
        buy_price = backtest["Price"].iloc[i]
        buy_shares = backtest["Shares"].iloc[i]
    elif action == "SELL THE SHARES AT CLOSE PRICE":
        sell_date = backtest.index[i]
        sell_price = backtest["Price"].iloc[i]
        profit = (sell_price*0.999-1.001*buy_price)*buy_shares
        trade_log.append({"Buy Date": buy_date,"Sell Date": sell_date,"Buy Price": buy_price,"Sell Price": sell_price,"Shares": buy_shares,"Profit": profit})
trade_log = pd.DataFrame(trade_log)
print(trade_log)

def trade_statistics(trade_log):
    numberoftrades = len(trade_log)
    winrate = len(trade_log[trade_log["Profit"]>0])/len(trade_log)
    average_win_amount = trade_log[trade_log["Profit"]>0]["Profit"].mean()
    average_loss_amount = trade_log[trade_log["Profit"]<0]["Profit"].mean()
    profit_factor = trade_log[trade_log["Profit"]>0]["Profit"].sum()/trade_log[trade_log["Profit"]<0]["Profit"].sum()
    return numberoftrades,winrate,average_win_amount,average_loss_amount,profit_factor

numberoftrades,winrate,average_win_amount,average_loss_amount,profit_factor = trade_statistics(trade_log)

def strategy_report(equity_curve,trade_log):
    content = f"""
# Backtest Report

    Strategy: SMA Crossover (50/200)
    Stock: RELIANCE.NS
    Period: 2021-05-25 to 2026-05-25
    _________________________________
    Total Return: {round(total_return(equity_curve)*100,2)}%
    Annualized Return: {round(annualized_return(equity_curve)*100,2)}%
    Sharpe Ratio: {sharpe}
    Max Drawdown: {round(maxi_drawdown*100,2)}%
    Win Rate: {round(winrate*100,2)}%
    Number of Trades: {numberoftrades}
    _________________________________
    """
    with open(r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\reports\RELIANCE_SMA_report.md","w") as file:
        file.write(content)
    return

strategy_report(equity_curve,trade_log)