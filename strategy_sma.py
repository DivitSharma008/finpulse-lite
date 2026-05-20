import pandas as pd
from datetime import date,timedelta
def generate_signals(df):
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")
    fiftydayMA = df["Close"].rolling(window="50D").mean()
    twohundreddayMA = df["Close"].rolling(window="200D").mean()
    signals = pd.Series(data=-1,index=df.index)
    signals.loc[fiftydayMA>twohundreddayMA] = 1    
    signals = signals.shift(1)
    print(signals)
    # print(signals[signals == 1])
reliance = pd.read_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\RELIANCE.csv")
generate_signals(reliance)
