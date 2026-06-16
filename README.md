# 📈 FinPulse: Algorithmic Trading Backtester

A Python-based backtesting framework for evaluating technical trading strategies on Indian stock market data (NSE). FinPulse supports multiple trading strategies and provides both a command-line interface (CLI) for scripted runs and an interactive Streamlit web interface for exploration, parameter tuning, and visualization.

---

## 📋 Table of contents

1. Project overview
2. Highlights
3. Project structure (expanded)
4. Supported stocks
5. Built-in strategies
6. Backtesting engine & assumptions
7. Performance metrics
8. Installation
9. Usage
   - Streamlit web dashboard
   - CLI mode
10. LeaderBoard and batch backtests
11. Configuration
12. Outputs & example report
13. Troubleshooting
14. Testing & development notes
15. Roadmap
16. Contribution & license

---

## 1. 🔭 Project overview

FinPulse is designed for researchers, traders, and students who want a lightweight but extensible toolkit to:
- implement and validate rule-based trading strategies on historical Indian market data,
- compare strategy performance against a buy-and-hold benchmark, and
- interactively explore strategy parameters and results using a Streamlit dashboard.

Key design goals:
- ♻️ Reproducible backtests with cached historical data
- 🧩 Modular strategy API so new indicators and rules can be added easily
- 🎯 Simple, opinionated execution model to keep results interpretable
- 🖥️ Usable both programmatically (CLI) and interactively (Streamlit)


## 2. ✨ Highlights

- 🖱️ Streamlit interactive dashboard for real-time parameter tuning and visualization
- 🏆 LeaderBoard to run and compare batch backtests across all supported symbols and strategies
- 📐 Built-in SMA and RSI strategies with configurable parameters
- 📊 Performance metrics: Sharpe ratio, annualized return, max drawdown, win rate, profit factor
- 💾 Exportable reports and trade logs (CSV / Markdown)
- ⚡ Caching of downloaded OHLCV data for fast repeated runs
- ✅ Unit-tested core modules (pytest) with coverage reporting


## 3. 🗂️ Project structure (expanded)

```
finpulse-lite/
├── app.py                  # Streamlit web interface (interactive dashboard)
├── main.py                 # CLI entry point for batch processing
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # Stock data fetching and management
│   ├── strategies.py       # Technical analysis strategy implementations
│   ├── backtester.py       # Backtesting engine
│   ├── metrics.py          # Performance calculation utilities
│   └── reporting.py        # Report generation
├── data/                   # Historical stock data (CSV files, gitignored)
├── reports/                # Generated markdown and CSV reports
├── images/                 # Saved equity curve charts
├── tests/                  # Unit tests (pytest)
└── notes/                  # Development notes and learning journal
```

Detailed descriptions:

- 🌐 **app.py** — Streamlit dashboard
  - Implements the interactive UI (Home Tab and LeaderBoard Tab).
  - Home tab: select stock and strategy, tune parameters via sliders, run backtest, view equity curve and trade statistics.
  - LeaderBoard tab: run batch backtests across all stocks and strategies, view ranked top/bottom 10 by Sharpe ratio, export CSV.
  - Uses `@st.cache_data` to avoid re-downloading OHLCV data and to speed up repeated backtests.

- 📥 **src/data_loader.py** — data fetching & caching
  - Wraps yfinance to fetch OHLCV data for NSE-listed stocks (`.NS` suffix).
  - Caches data to `data/` as CSV files to make re-runs deterministic and fast.
  - Key functions: `load_data(symbol)`, `get_stock_name(symbol)`.
  - `STOCKS` dict maps friendly names (e.g. `"TCS"`) to Yahoo Finance tickers (e.g. `"TCS.NS"`).

- 🧠 **src/strategies.py** — strategy implementations
  - `generate_signals(symbol)`: SMA crossover — buys when 50-day SMA crosses above 200-day, sells on cross below.
  - `generate_rsi_signals(symbol, period, oversold, overbought)`: RSI-based entries/exits using EWM smoothing.
  - Both functions return a `pd.Series` of signals (1 = buy, -1 = sell, 0 = hold) with a 1-day lag to avoid lookahead bias.

- ⚙️ **src/backtester.py** — core backtesting engine
  - `run_backtest(df, signals, initial_capital=100000)`: iterates over price data and signals to produce an equity curve.
  - Execution model: signals act on the same bar's close price (all-in / all-out, long only).
  - Commission: 0.1% on buy, 0.1% on sell, applied via `Adjusted Portfolio` column.
  - Returns a DataFrame with columns: `Action`, `Price`, `Shares`, `Cash`, `Portfolio`, `Adjusted Portfolio`.

- 📐 **src/metrics.py** — performance calculations
  - `total_return`, `annualized_return`, `max_drawdown`, `sharpe_ratio` (risk-free rate = 6.5%).
  - `build_trade_log(backtest)`: extracts per-trade buy/sell pairs with profit.
  - `trade_statistics(trade_log)`: returns num_trades, win_rate, profit_factor.

- 📄 **src/reporting.py** — report & export
  - `strategy_report(equity_curve, trade_log, symbol, strategy_name)`: generates a Markdown report saved to `reports/`.

- 🧪 **tests/** — unit tests
  - 10 handbook-specified tests written as flat functions (no classes), covering data loading, signal generation, backtester logic, and metrics.
  - Run with `pytest` or `pytest --cov=src` for coverage.


## 4. 🏦 Supported stocks

FinPulse currently supports 10 NSE blue-chip symbols: RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, SBIN, ITC, LT, HINDUNILVR, KOTAKBANK.

You can add more by extending the `STOCKS` dictionary in `src/data_loader.py` with any valid Yahoo Finance `.NS` ticker.


## 5. 🧠 Built-in strategies (detailed)

### 📉 SMA (Simple Moving Average crossover)
- **Logic:** the 50-day SMA crossing above the 200-day SMA produces a buy; crossing below produces a sell.
- **Parameters:** fast_window (default 50), slow_window (default 200).
- **Minimum history:** at least 200 trading days.
- **Signal lag:** 1 day applied via `.shift(1)` to avoid lookahead bias.

### 📈 RSI (Relative Strength Index)
- **Logic:** momentum-based entries using RSI (default 14-period, EWM smoothing). Buy when RSI < oversold threshold (default 30); sell when RSI > overbought threshold (default 70).
- **Parameters:** period (int, default 14), oversold (int, default 30), overbought (int, default 70).
- **Signal lag:** 1 day applied via `.shift(1)`.

➕ **How to add a new strategy:**
- Implement a function that accepts a `symbol` string and returns a `pd.Series` of signals (1/-1/0) aligned to the stock's date index, with a 1-day lag.
- Register it in `SUPPORTED_STRATEGIES` in `strategies.py`.


## 6. ⚙️ Backtesting engine & assumptions

Important assumptions to keep results reproducible and understandable:
- 🕐 **Execution model:** trades execute at the close price of the bar on which the signal fires (signal is already lagged by 1 day, so no lookahead bias).
- 💰 **Position size:** single position at a time; when a buy signal fires, the engine invests all available cash (all-in). On sell, it liquidates fully.
- 🚫 **No shorting:** only long positions are supported.
- 💸 **Commission:** 0.1% on buy side (price × 1.001), 0.1% on sell side (price × 0.999). Reflected in `Adjusted Portfolio`.
- 🚫 No partial fills, margin, or leverage are modeled.
- ⚠️ **Signal count ≠ trade executions:** the backtester only acts on signal *transitions* (0→1 for buy, 1→-1 for sell), not every day a signal is active.

Trade log columns: Buy Date, Sell Date, Buy Price, Sell Price, Shares, Profit.


## 7. 📊 Performance metrics

- 📐 **Sharpe Ratio:** risk-adjusted return (risk-free rate = 6.5% annual, Indian T-bill approximation). >1 is reasonable, >2 is strong.
- 💹 **Total Return:** percentage change in equity from start to finish.
- 📅 **Annualized Return:** CAGR — `((final / initial) ** (1 / years)) - 1`.
- 📉 **Max Drawdown:** largest peak-to-trough percentage decline (always ≤ 0).
- 🎯 **Win Rate:** % of closed trades with positive P&L.
- ⚖️ **Profit Factor:** gross profit / gross loss (>1 means profitable overall).


## 8. 🛠️ Installation

Requirements:
- Python 3.7+
- See `requirements.txt` for dependencies (pandas, numpy, yfinance, matplotlib, plotly, streamlit)

Setup:

```bash
git clone https://github.com/DivitSharma008/finpulse-lite.git
cd finpulse-lite
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```


## 9. 🚀 Usage

### 🌐 Streamlit web dashboard (recommended)

Start the interface:

```bash
streamlit run app.py
```

Interface overview:
- 🏠 **Home tab:** pick a stock from the sidebar, choose a strategy, tune parameters (SMA windows or RSI period/thresholds), check "Run backtester" to see the equity curve, metrics, and trade table.
- 🏆 **LeaderBoard tab:** click "Run All Backtests" to iterate all supported stocks × both strategies. Results ranked by Sharpe ratio with top 10 and bottom 10 tables. Export as CSV.


### 💻 CLI mode

Run a single backtest:

```bash
python -m src.backtester   # or python -m src.metrics / src.reporting
```

Follow the interactive prompts for symbol and strategy. Outputs a Markdown report to `reports/` and prints metrics to the terminal.


## 10. 🏆 LeaderBoard & batch backtests

The LeaderBoard tab evaluates strategy performance across the supported stock universe:
- 🔄 Iterates all stocks and both strategies (SMA + RSI)
- ⚡ Uses `@st.cache_data` — subsequent runs are near-instant after the first download
- 💾 Results stored in `st.session_state.backtest_results` and persist for the session
- 🥇 Ranked by Sharpe ratio; filter by strategy via radio buttons
- 📊 Summary statistics (avg Sharpe, avg return, best Sharpe, best return) shown below the tables
- 📥 Export the full leaderboard as a dated CSV


## 11. 🔧 Configuration

Defaults are set in `src/data_loader.py` and `src/backtester.py`. Common knobs:
- `STOCKS` (dict in `data_loader.py`) — add or remove tickers here
- `START`, `END` (data_loader.py) — default lookback is 5 years from today
- `initial_capital` (backtester.py `run_backtest`) — default ₹1,00,000
- Commission: 0.1% buy / 0.1% sell (hardcoded in `run_backtest`; update the `1.001`/`0.999` multipliers to change)

All file paths are constructed with `os.path.join()` relative to the project root — no hardcoded absolute paths.


## 12. 📄 Outputs & example report

Reports are saved to `reports/` as Markdown files. Example:

```
# Backtest Report

Strategy         : SMA STRATEGY
Stock            : TCS.NS
Period           : 2021-06-05 -> 2026-06-05
________________________________________________
Total Return     : 145.32%
Annualized Return: 19.85%
Sharpe Ratio     : 1.45
Max Drawdown     : -32.15%
Win Rate         : 58.33%
Number of Trades : 24
________________________________________________
```


## 13. 🐛 Troubleshooting

- ❓ **"No data returned for 'X'":** verify the ticker exists on Yahoo Finance or add it to `STOCKS` in `src/data_loader.py`.
- ❓ **"Not enough data to calculate 200-day SMA":** the stock may not have 5 years of history — try reducing `slow_window` or extending `START`.
- ❓ **"KeyError: Unknown symbol":** the symbol is not in the `STOCKS` dict. Add it or use the correct `.NS` ticker.
- 🌐 **"Network error / empty DataFrame from yfinance":** confirm internet access. yfinance occasionally has rate-limit issues — wait and retry.
- 🔄 **Streamlit cache not updating:** run `streamlit cache clear` or restart the app. You can also clear cache from the Streamlit hamburger menu.
- ⚠️ **Metrics showing `nan` or `inf`:** usually caused by a strategy with zero trades (flat equity curve) — `annualized_return` and `sharpe_ratio` guard against division by zero.


## 14. 🧪 Testing & development notes

Unit tests live in `tests/`. The 10 handbook-specified tests cover:
- 📥 Data loading and CSV output
- 📐 SMA and RSI signal generation (correct values, correct length, 1-day lag)
- ⚙️ Backtester logic (buy/sell action detection, equity curve monotonicity)
- 📊 Metrics (total return, Sharpe ratio edge cases)

Run tests:
```bash
pytest                        # run all tests
pytest --cov=src              # with coverage report
pytest -v                     # verbose output
```

> ⚠️ When a test fails, report the bug in the source module — do not modify the test to pass.


## 15. 🗺️ Roadmap

Planned enhancements:
- 📈 Expand stock universe to full NIFTY 50
- 🔀 Multiple position support and position sizing rules
- 🔍 Parameter optimization (grid search) and walk-forward testing
- 📉 Additional indicators (MACD, Bollinger Bands)
- ☁️ Streamlit Cloud deployment


## 16. 🤝 Contribution & license

This project is part of the FinPulse Intern Program (Handbook Edition 2). Contributions and forks are welcome.

> ⚠️ **Disclaimer:** This framework is for educational and research purposes only. Past performance is not indicative of future results. Consult a financial professional before making trading decisions.

---

**Last Updated**: June 16 2026  
**Version**: 2.2
