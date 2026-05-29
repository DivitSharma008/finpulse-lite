import pandas as pd

def generate_signals(df):
    df = df.copy()

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], utc=True)
        df = df.set_index("Date")
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
        df.index = pd.to_datetime(df.index.date)

    fiftydayMA      = df["Close"].rolling(window=50).mean()
    twohundreddayMA = df["Close"].rolling(window=200).mean()

    signals = pd.Series(data=0, index=df.index)
    signals.loc[fiftydayMA > twohundreddayMA] =  1
    signals.loc[fiftydayMA < twohundreddayMA] = -1
    signals = signals.shift(1).fillna(0)

    return signals

reliance = pd.read_csv(r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\data\RELIANCE.csv")
signals  = generate_signals(reliance)
