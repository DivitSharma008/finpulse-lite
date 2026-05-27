import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from datetime import date,timedelta
from backtest import backtest

def total_return(equity_curve):
    return (equity_curve.iloc[-1]/equity_curve.iloc[0]-1)

def annualized_return(equity_curve):
    years = (equity_curve.index[-1]-equity_curve.index[0]).days/365
    return(((equity_curve.iloc[-1]/equity_curve.iloc[0])**(1/years))-1)

print("The total return is",round(total_return(backtest["Adjusted Portfolio"])*100,2),"%")
print("The annualized return is",round(annualized_return(backtest["Adjusted Portfolio"])*100,2),"%")


def max_drawdown(equity_curve):
    maxtillnow = equity_curve.cummax()
    drawdown = equity_curve/maxtillnow-1
    maxi_drawdown = drawdown.min()
    return maxi_drawdown,equity_curve.loc[:equity_curve.idxmin()].idxmax(),equity_curve.idxmin(),drawdown

maxi_drawdown,start_date,end_date,drawdown=max_drawdown(backtest["Adjusted Portfolio"])
print("The maximum drawdown is ",round(maxi_drawdown*100,2),"%")
print("The starting and ending dates are ",start_date,"and",end_date)

plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.title("Daily Drawdown")
plt.plot(drawdown)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()