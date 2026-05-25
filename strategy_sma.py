import pandas as pd
from datetime import date,timedelta
def generate_signals(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")
    fiftydayMA = df["Close"].rolling(window=50).mean()
    twohundreddayMA = df["Close"].rolling(window=200).mean()
    signals = pd.Series(data=0,index=df.index)
    signals.loc[fiftydayMA>twohundreddayMA] = 1
    signals.loc[fiftydayMA<twohundreddayMA] = -1   
    signals = signals.shift(1).fillna(0)
    return signals
    # print(signals[signals == 1])
reliance = pd.read_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\RELIANCE.csv")
signals = generate_signals(reliance)
