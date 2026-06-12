import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from src.data_loader import STOCKS,get_stock_name
from src.strategies import generate_signals
from src.backtester import run_backtest
from src.metrics import build_trade_log

st.title("My basic app with a title")
add_selectbox = st.sidebar.selectbox(
    'Pick the stock symbol!',
    STOCKS.values()
)
name = get_stock_name(add_selectbox)
my_chart = pd.read_csv(fr"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\data\{name}.csv")
my_signals = generate_signals(add_selectbox)
st.line_chart(my_chart,x="Date",y="Close")

if st.checkbox("Run backtester"):
    st.subheader("Backtest")
    backtest = run_backtest(my_chart,my_signals)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=backtest["Date"],y=backtest["Adjusted Portfolio"]))
    fig.update_layout(
    xaxis=dict(
        type='date',
        tickformat='%b %d, %Y',  # Formats as 'Jan 01, 2026'
    )
)
    fig.update_layout(title="Last 5 Years - Adjusted Portfolio",xaxis_title="Date",yaxis_title="Adjusted Portfolio")
    st.plotly_chart(fig)
    trade_log = build_trade_log(backtest)

    st.subheader("Some metrics")
    st.table(data=trade_log)