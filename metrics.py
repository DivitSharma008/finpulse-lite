import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date,timedelta
from backtest import backtest,run_backtest

def total_return(equity_curve):
    return (equity_curve.iloc[-1]/equity_curve.iloc[0]-1)

def annualized_return(equity_curve):
    years = (equity_curve.index[-1]-equity_curve.index[0]).days/365
    return(((equity_curve.iloc[-1]/equity_curve.iloc[0])**(1/years))-1)

print("The total return is",round(total_return(backtest["Adjusted Portfolio"])*100,2),"%")
print("The annualized return is",round(annualized_return(backtest["Adjusted Portfolio"])*100,2),"%")