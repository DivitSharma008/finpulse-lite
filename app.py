import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import date
from src.data_loader import STOCKS, get_stock_name, load_data
from src.strategies import generate_signals, generate_rsi_signals, SUPPORTED_STRATEGIES
from src.backtester import run_backtest
from src.metrics import (
    build_trade_log,
    trade_statistics,
    sharpe_ratio,
    total_return,
    max_drawdown,
    annualized_return,
)

st.set_page_config(page_title="FinPulse", page_icon="📈", layout="wide")
st.title("📈 FinPulse Backtester")

# ============================================================================
# CACHED FUNCTIONS (Load once, reuse)
# ============================================================================


@st.cache_data
def load_stock_data(symbol):
    """Cache stock data - loads only once per symbol"""
    path = load_data(symbol)
    return pd.read_csv(rf"{path}", index_col="Date", parse_dates=True)


@st.cache_data
def get_sma_signals(symbol, slow_window, fast_window):
    """Cache SMA signals - calculates only once per params"""
    return generate_signals(symbol, slow_window, fast_window)


@st.cache_data
def get_rsi_signals(symbol, period, oversold, overbought):
    """Cache RSI signals - calculates only once per params"""
    return generate_rsi_signals(symbol, oversold, overbought, period)


@st.cache_data
def run_cached_backtest(
    symbol,
    strategy,
    slow_window=200,
    fast_window=50,
    period=14,
    oversold=30,
    overbought=70,
):
    """Cache backtest results - runs only once per params"""
    my_chart = load_stock_data(symbol)

    if strategy == "SMA":
        signals = get_sma_signals(symbol, slow_window, fast_window)
    else:  # RSI
        signals = get_rsi_signals(symbol, period, oversold, overbought)

    return run_backtest(my_chart, signals)


# ============================================================================
# Initialize session state
# ============================================================================

if "backtest_results" not in st.session_state:
    st.session_state.backtest_results = []

Home, LeaderBoard = st.tabs(["Home", "LeaderBoard"])

# ============================================================================
# HOME TAB
# ============================================================================

with Home:
    col1, col2 = st.columns([2, 3])

    with col1:
        symbol = st.sidebar.selectbox("Pick the stock symbol!", STOCKS.values())
        name = get_stock_name(symbol)

    with col2:
        st.write("")

    # Load data (cached)
    my_chart = load_stock_data(symbol)

    st.subheader("Daily Close Price")
    st.line_chart(my_chart, y="Close")

    st.divider()

    st.header("Strategy")

    col1, col2 = st.columns(2)

    with col1:
        strategy_name = st.selectbox("Choose strategy:", SUPPORTED_STRATEGIES)

    with col2:
        st.write("")

    if strategy_name == "SMA":
        col1, col2 = st.columns(2)
        with col1:
            slow_window = st.slider(
                "SMA Slow Window", min_value=5, max_value=300, value=200
            )
        with col2:
            fast_window = st.slider(
                "SMA Fast Window", min_value=5, max_value=slow_window // 2, value=50
            )

    elif strategy_name == "RSI":
        col1, col2, col3 = st.columns(3)
        with col1:
            period = st.slider("RSI Period", min_value=5, max_value=50, value=14)
        with col2:
            oversold = st.slider("Oversold", min_value=10, max_value=40, value=30)
        with col3:
            overbought = st.slider("Overbought", min_value=60, max_value=90, value=70)

    st.divider()

    if st.checkbox("Run backtester", value=False):
        st.subheader("Backtest Results")

        # Use cached backtest
        if strategy_name == "SMA":
            backtest = run_cached_backtest(symbol, "SMA", slow_window, fast_window)
        else:
            backtest = run_cached_backtest(
                symbol, "RSI", period=period, oversold=oversold, overbought=overbought
            )

        backtest["Buy & Hold"] = backtest["Close"] * (
            100000 / backtest["Close"].iloc[0]
        )

        # Calculate metrics
        equity_curve = pd.Series(
            backtest["Adjusted Portfolio"].values, index=pd.to_datetime(backtest.index)
        )
        trade_log = build_trade_log(backtest)
        stats = trade_statistics(trade_log)

        metrics = {
            "sharpe_ratio": sharpe_ratio(equity_curve),
            "total_return": total_return(equity_curve),
            "annualized_return": annualized_return(equity_curve),
            "max_drawdown": max_drawdown(equity_curve),
            "num_trades": stats["num_trades"],
            "win_rate": stats["win_rate"],
            "profit_factor": stats.get("profit_factor", 0),
        }

        # Store in session
        st.session_state.backtest_results = [
            r
            for r in st.session_state.backtest_results
            if not (r["Stock"] == name and r["Strategy"] == strategy_name)
        ]

        st.session_state.backtest_results.append(
            {"Stock": name, "Strategy": strategy_name, **metrics}
        )

        tab1, tab2 = st.tabs(["Strategy Performance", "Strategy vs Buy & Hold"])

        with tab1:
            fig = px.line(
                backtest,
                y="Adjusted Portfolio",
                labels={"value": "Portfolio Value"},
                title=f"{name} - {strategy_name} Strategy",
            )
            st.plotly_chart(fig, use_container_width=True)

            st.divider()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
            with col2:
                st.metric("Total Return", f"{metrics['total_return']*100:.2f}%")
            with col3:
                st.metric("Max Drawdown", f"{metrics['max_drawdown']*100:.2f}%")
            with col4:
                st.metric(
                    "Annualized Return", f"{metrics['annualized_return']*100:.2f}%"
                )

            st.divider()

            st.subheader("Trade Statistics")
            st.table(stats)

        with tab2:
            fig = px.line(
                backtest,
                y=["Adjusted Portfolio", "Buy & Hold"],
                labels={
                    "value": "Portfolio Value",
                    "variable": "Strategy",
                    "Adjusted Portfolio": f"{strategy_name}",
                },
                title=f"{name} - Strategy vs Buy & Hold",
            )
            fig.for_each_trace(
                lambda t: t.update(
                    name=strategy_name if t.name == "Adjusted Portfolio" else t.name
                )
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# LEADERBOARD TAB
# ============================================================================

with LeaderBoard:
    st.subheader("🏆 Leaderboard")

    st.write("**Strategy Parameters**")
    col_sma1, col_sma2, col_rsi1, col_rsi2, col_rsi3 = st.columns(5)

    with col_sma1:
        lb_slow_window = st.slider(
            "SMA Slow Window", min_value=5, max_value=300, value=200, key="lb_slow"
        )
    with col_sma2:
        lb_fast_window = st.slider(
            "SMA Fast Window",
            min_value=5,
            max_value=lb_slow_window // 2,
            value=50,
            key="lb_fast",
        )
    with col_rsi1:
        lb_period = st.slider(
            "RSI Period", min_value=5, max_value=50, value=14, key="lb_period"
        )
    with col_rsi2:
        lb_oversold = st.slider(
            "Oversold", min_value=10, max_value=40, value=30, key="lb_oversold"
        )
    with col_rsi3:
        lb_overbought = st.slider(
            "Overbought", min_value=60, max_value=90, value=70, key="lb_overbought"
        )

    st.divider()

    # Button to run all backtests
    col1, col2 = st.columns([1, 4])

    with col1:
        if st.button("▶️ Run All Backtests", use_container_width=True):
            st.info("⚡ Running backtests for all 50 stocks (using cached data)...")

            progress_bar = st.progress(0)
            status_text = st.empty()

            total_stocks = len(STOCKS)

            for idx, (stock_name, symbol) in enumerate(STOCKS.items()):
                for strategy in ["SMA", "RSI"]:
                    try:
                        # Use cached backtest (much faster on second run)
                        if strategy == "SMA":
                            backtest = run_cached_backtest(
                                symbol, "SMA", lb_slow_window, lb_fast_window
                            )
                        else:
                            backtest = run_cached_backtest(
                                symbol,
                                "RSI",
                                period=lb_period,
                                oversold=lb_oversold,
                                overbought=lb_overbought,
                            )

                        # Calculate metrics
                        equity_curve = pd.Series(
                            backtest["Adjusted Portfolio"].values,
                            index=pd.to_datetime(backtest.index),
                        )
                        trade_log = build_trade_log(backtest)
                        stats = trade_statistics(trade_log)

                        metrics = {
                            "sharpe_ratio": sharpe_ratio(equity_curve),
                            "total_return": total_return(equity_curve),
                            "annualized_return": annualized_return(equity_curve),
                            "max_drawdown": max_drawdown(equity_curve),
                            "num_trades": stats["num_trades"],
                            "win_rate": stats["win_rate"],
                            "profit_factor": stats.get("profit_factor", 0),
                        }

                        # Store in session (FIX: use stock_name and strategy instead of undefined name and strategy_name)
                        st.session_state.backtest_results = [
                            r
                            for r in st.session_state.backtest_results
                            if not (
                                r["Stock"] == stock_name and r["Strategy"] == strategy
                            )
                        ]

                        st.session_state.backtest_results.append(
                            {"Stock": stock_name, "Strategy": strategy, **metrics}
                        )

                        # Update progress
                        progress = (idx * 2 + (1 if strategy == "RSI" else 0)) / (
                            total_stocks * 2
                        )
                        progress_bar.progress(progress)
                        status_text.text(f"✓ {stock_name} ({strategy})")

                    except Exception as e:
                        status_text.text(f"❌ Error with {stock_name} ({strategy})")
                        continue

            progress_bar.progress(1.0)
            st.success("✅ All backtests completed! (Results cached for future runs)")

    with col2:
        st.write("")

    st.divider()

    # Display results
    if not st.session_state.backtest_results:
        st.info("📊 Click 'Run All Backtests' to populate the leaderboard!")
    else:
        # Convert to dataframe
        results_df = pd.DataFrame(st.session_state.backtest_results)

        # Filter by strategy
        strategy_filter = st.radio(
            "Filter by Strategy:", ["All"] + list(SUPPORTED_STRATEGIES), horizontal=True
        )

        if strategy_filter == "All":
            display_df = results_df
        else:
            display_df = results_df[results_df["Strategy"] == strategy_filter]
        st.divider()
        if display_df.empty:
            st.info(f"No {strategy_filter} backtests yet!")

        else:
            # Sort by sharpe ratio
            display_df = display_df.sort_values(
                "sharpe_ratio", ascending=False
            ).reset_index(drop=True)
            display_df.insert(0, "Rank", range(1, len(display_df) + 1))

            col1, col2 = st.columns(2)

            with col1:
                st.write("**📈 Top 10 Performers**")
                top_10 = display_df.head(10)[
                    [
                        "Rank",
                        "Stock",
                        "Strategy",
                        "sharpe_ratio",
                        "total_return",
                        "num_trades",
                    ]
                ]
                top_10_display = top_10.copy()
                top_10_display.columns = [
                    "Rank",
                    "Stock",
                    "Strategy",
                    "Sharpe",
                    "Return %",
                    "Trades",
                ]
                top_10_display["Return %"] = (top_10_display["Return %"] * 100).round(2)
                top_10_display["Sharpe"] = top_10_display["Sharpe"].round(2)
                st.dataframe(top_10_display, use_container_width=True, hide_index=True)

            with col2:
                st.write("**📉 Bottom 10 Performers**")
                bottom_10 = display_df.tail(10)[
                    [
                        "Rank",
                        "Stock",
                        "Strategy",
                        "sharpe_ratio",
                        "total_return",
                        "num_trades",
                    ]
                ]
                bottom_10_display = bottom_10.copy()
                bottom_10_display.columns = [
                    "Rank",
                    "Stock",
                    "Strategy",
                    "Sharpe",
                    "Return %",
                    "Trades",
                ]
                bottom_10_display["Return %"] = (
                    bottom_10_display["Return %"] * 100
                ).round(2)
                bottom_10_display["Sharpe"] = bottom_10_display["Sharpe"].round(2)
                st.dataframe(
                    bottom_10_display, use_container_width=True, hide_index=True
                )

            st.divider()

            # Summary stats
            st.subheader("📊 Summary Statistics")
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("Total Backtests", len(display_df))
            with col2:
                st.metric("Avg Sharpe", f"{display_df['sharpe_ratio'].mean():.2f}")
            with col3:
                st.metric("Avg Return", f"{display_df['total_return'].mean()*100:.2f}%")
            with col4:
                st.metric("Best Sharpe", f"{display_df['sharpe_ratio'].max():.2f}")
            with col5:
                st.metric("Best Return", f"{display_df['total_return'].max()*100:.2f}%")

            st.divider()

            # Download button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Leaderboard (CSV)",
                data=csv,
                file_name=f"leaderboard_{strategy_filter}_{date.today()}.csv",
                mime="text/csv",
            )
