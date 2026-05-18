import yfinance as yf
from datetime import date,timedelta

reliance = yf.Ticker("Reliance.ns")
tcs = yf.Ticker("TCS.ns")
infy = yf.Ticker("INFY.ns")
hdfcbank = yf.Ticker("HDFCBANK.ns")
icicibank = yf.Ticker("ICICIBANK.ns")
sbi = yf.Ticker("SBIN.ns")
try:
    itc = yf.Ticker("ITC.ns")
except :
    print("STOCK NOT AVAILABLE")
lt = yf.Ticker("LT.ns")
hindunilvr = yf.Ticker("HINDUNILVR.ns")
kotakbank = yf.Ticker("KOTAKBANK.ns")

# print(reliance)
# print(reliance_historical.head(10))
# print(reliance_historical.columns)

reliance_historical = reliance.history(start = date.today()-timedelta(days =5*365),end = date.today())
tcs_historical = tcs.history(start = date.today()-timedelta(days =5*365),end = date.today())
infy_historical = infy.history(start = date.today()-timedelta(days =5*365),end = date.today())
hdfcbank_historical = hdfcbank.history(start = date.today()-timedelta(days =5*365),end = date.today())
icicibank_historical = icicibank.history(start = date.today()-timedelta(days =5*365),end = date.today())
sbi_historical = sbi.history(start = date.today()-timedelta(days =5*365),end = date.today())
itc_historical = itc.history(start = date.today()-timedelta(days =5*365),end = date.today())
lt_historical = lt.history(start = date.today()-timedelta(days =5*365),end = date.today())
hindunilvr_historical = hindunilvr.history(start = date.today()-timedelta(days =5*365),end = date.today())
kotakbank_historical = kotakbank.history(start = date.today()-timedelta(days =5*365),end = date.today())

reliance_historical.to_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\RELIANCE.csv")
tcs_historical.to_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\TCS.csv")
infy_historical.to_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\INFY.csv")
hdfcbank_historical.to_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\HDFCBANK.csv")
icicibank_historical.to_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\ICICIBANK.csv")
sbi_historical.to_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\SBIN.csv")
itc_historical.to_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\ITC.csv")
lt_historical.to_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\LT.csv")
hindunilvr_historical.to_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\HINDUNILVR.csv")
kotakbank_historical.to_csv("C:\\Users\DELL\OneDrive\Desktop\\finpulse-lite\data\KOTAKBANK.csv")
