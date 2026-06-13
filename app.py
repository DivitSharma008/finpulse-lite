import streamlit as st
import streamlit_authenticator as stauth
import plotly.express as px
import pandas as pd
from datetime import date
from src.data_loader import STOCKS,get_stock_name
from src.strategies import generate_signals,generate_rsi_signals,SUPPORTED_STRATEGIES
from src.backtester import run_backtest
from src.metrics import build_trade_log,trade_statistics


st.title("My basic app with a title")
add_selectbox = st.sidebar.selectbox(
    'Pick the stock symbol!',
    STOCKS.values()
)

name = get_stock_name(add_selectbox)
my_chart = pd.read_csv(fr"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\data\{name}.csv")

st.header("Strategy")
strategy_name = st.selectbox("Choose strategy(SMA Crossover/RSI):",SUPPORTED_STRATEGIES)
if strategy_name == "SMA":
    slow_window = st.slider("SMA Slow Window",min_value=5,max_value=5*365)
    fast_window = st.slider("SMA Fast Window",min_value=1,max_value=slow_window)
    my_signals = generate_signals(add_selectbox,slow_window,fast_window)
elif strategy_name == "RSI":
    period = st.slider("RSI Period",min_value=5,max_value=5*365)
    oversold = st.slider("Oversold",min_value=1,max_value=99)
    overbought = st.slider("Overbought",min_value=oversold,max_value=99)
    my_signals = generate_rsi_signals(add_selectbox,oversold,overbought,period)

st.subheader("Daily Close Price")
st.line_chart(my_chart,x="Date",y="Close")

if st.checkbox("Run backtester"):
    st.subheader("Backtest")
    backtest = run_backtest(my_chart,my_signals)
    backtest["Buy & Hold"] = backtest["Close"] * (100000 / backtest["Close"].iloc[0])
    tab1,tab2 = st.tabs(["Strategy Performance","Strategy vs Buy & Hold"])
    with tab1:
        fig = px.line(backtest,x="Date",y="Adjusted Portfolio",labels={"value":"Portfolio Value"})
        st.plotly_chart(fig)
        trade_log = build_trade_log(backtest)
        stats = trade_statistics(trade_log)

        st.subheader("Some metrics")
        st.table(data=stats)

    with tab2:
        fig = px.line(backtest,x="Date",y=["Adjusted Portfolio","Buy & Hold"],labels={"value":"Portfolio Value","variable":"Legend"})
        st.plotly_chart(fig)
    
    