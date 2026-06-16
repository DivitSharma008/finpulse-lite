# 📈 FinPulse: Algorithmic Trading Backtester

A Python-based backtesting framework for evaluating technical trading strategies on Indian stock market data (NSE). FinPulse supports multiple trading strategies and provides both a command-line interface (CLI) for scripted runs and an interactive Streamlit web interface for exploration, parameter tuning, and visualization.

---

## Table of contents

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

## 1. Project overview

FinPulse is designed for researchers, traders, and students who want a lightweight but extensible toolkit to:
- implement and validate rule-based trading strategies on historical Indian market data,
- compare strategy performance against a buy-and-hold benchmark, and
- interactively explore strategy parameters and results using a Streamlit dashboard.

Key design goals:
- Reproducible backtests with cached historical data
- Modular strategy API so new indicators and rules can be added easily
- Simple, opinionated execution model to keep results interpretable
- Usable both programmatically (CLI) and interactively (Streamlit)


## 2. Highlights

- Streamlit interactive dashboard for real-time parameter tuning and visualization
- LeaderBoard to run and compare batch backtests across many symbols and strategies
- Built-in SMA and RSI strategies with configurable parameters
- Performance metrics: Sharpe ratio, annualized return, max drawdown, win rate, profit factor
- Exportable reports and trade logs (CSV / Markdown)
- Caching of downloaded OHLCV data for fast repeated runs


## 3. Project structure (expanded)

```
finpulse-lite/
├── app.py                  # Streamlit web interface (interactive dashboard)
├── main.py                 # CLI entry point for batch processing
├── plot_stock.py           # Stock price visualization utility
├── requirements.txt        # Python dependencies
├── src/
│   ├── data_loader.py      # Stock data fetching and management
│   ├── strategies.py       # Technical analysis strategy implementations
│   ├── backtester.py       # Backtesting engine
│   ├── metrics.py          # Performance calculation utilities
│   └── reporting.py        # Report generation
├── data/                   # Historical stock data (CSV files, cached)
├── reports/                # Generated markdown and CSV reports
├── tests/                  # Unit tests
└── notes/                  # Development notes
```

Detailed descriptions:

- app.py — Streamlit dashboard
  - Implements the interactive UI (Home Tab and LeaderBoard Tab).
  - Responsible for collecting user inputs (symbol, strategy, parameters, date range), invoking the backtester, and displaying charts and tables.
  - Uses caching to avoid re-downloading OHLCV data and to speed up repeated backtests.

- main.py — CLI entrypoint
  - Lightweight command-line interface for scripted or one-off backtests.
  - Prompts for symbol/strategy when run interactively or accepts arguments for automation.
  - Produces the same report files as the Streamlit UI for consistency.

- plot_stock.py — visualization helpers
  - Shared plotting utilities used by both the Streamlit app and CLI report generation.
  - Contains functions to draw price series, equity curves, and trade markers.

- src/data_loader.py — data fetching & caching
  - Wraps yfinance (or other data sources) to fetch OHLCV data.
  - Provides caching to `data/` as CSV files to make re-runs deterministic and fast.
  - Key functions: fetch_symbol(symbol, start, end), load_cached(symbol, start, end).

- src/strategies.py — strategy implementations
  - Each strategy follows a simple interface: generate_signals(df: DataFrame, **params) -> DataFrame with a `signal` column (1 for long entry, 0 for flat/exit).
  - Built-in strategies include SMA crossover and RSI-based entries/exits.
  - To add a new strategy, implement the same function signature and return the signal column and any debug fields required.

- src/backtester.py — core backtesting engine
  - Takes OHLCV data and signals, runs through time to generate trades and equity curve.
  - Execution model: trades execute at the close price of the next bar after a signal (configurable).
  - Position sizing: single position at a time with configurable initial capital; default is all-in/all-out.
  - Commission and basic trade costs are applied per trade (default 0.1% buy, 0.1% sell).
  - Outputs a trade log DataFrame and an equity curve time series.

- src/metrics.py — performance calculations
  - Computes Sharpe ratio (configurable risk-free), annualized return, cumulative and periodic returns, max drawdown, win rate, and profit factor.

- src/reporting.py — report & export
  - Generates human-readable Markdown reports and machine-friendly CSV outputs for trades and summary metrics.
  - Used by both CLI and Streamlit LeaderBoard for consistent outputs.

- data/ and reports/ directories
  - data/ stores cached OHLCV CSVs to avoid repeated network requests.
  - reports/ holds generated backtest reports and CSV exports.


## 4. Supported stocks

By default FinPulse includes many Indian blue-chip symbols such as RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, SBIN, ITC, LT, HINDUNILVR, KOTAKBANK, and more. You can extend the supported set by adding additional ticker mappings in `src/data_loader.py` (the STOCKS dictionary) or by passing any valid Yahoo Finance symbol to the backtester.


## 5. Built-in strategies (detailed)

### SMA (Simple Moving Average crossover)
- Logic: a fast SMA (default 50-day) crossing above a slow SMA (default 200-day) produces a buy; crossing below produces a sell.
- Parameters: fast_window, slow_window (both integers).
- Minimum history: at least `slow_window` days to compute the slow SMA.
- Example usage: fast_window=50, slow_window=200.

### RSI (Relative Strength Index)
- Logic: momentum-based entries using RSI (default 14-period). Buy when RSI falls below the oversold threshold (default 30) and sell when RSI rises above the overbought threshold (default 70).
- Parameters: period (int), oversold (int), overbought (int).

How to add a new strategy:
- Implement `generate_signals(df, **params)` returning the original df with a standardized `signal` column (1 = long, 0 = flat) and document parameters in the function docstring.


## 6. Backtesting engine & assumptions

Important assumptions to keep results reproducible and understandable:
- Execution model: orders are filled at the closing price of the next bar following a signal by default (this keeps lookahead bias minimal).
- Position size: single position allowed at a time; when a buy signal generates, the engine invests the full available capital (all-in). On sell, it liquidates fully.
- No shorting: only long positions are currently supported.
- Slippage: not modeled aside from a per-trade commission. Commission defaults to 0.1% on both buy and sell.
- No partial fills, margin, or leverage are modeled currently.

Trade log format (example columns):
- entry_date, exit_date, entry_price, exit_price, quantity, pnl, cumulative_equity


## 7. Performance metrics

- Sharpe Ratio: risk-adjusted return (default risk-free = 6.5% annual). Interpret: >1 is reasonable, >2 is strong.
- Total Return: percentage change in equity from start to finish.
- Annualized Return: compounded annual growth rate.
- Max Drawdown: largest peak-to-trough percentage decline — smaller magnitude is better.
- Win Rate: % of trades with positive P&L.
- Profit Factor: gross profit / gross loss — >1 means profitable strategy.


## 8. Installation

Requirements:
- Python 3.7+
- See `requirements.txt` for pinned dependencies (pandas, numpy, yfinance, matplotlib, plotly, streamlit, etc.)

Setup:

```bash
git clone https://github.com/DivitSharma008/finpulse-lite.git
cd finpulse-lite
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```


## 9. Usage

### Streamlit web dashboard (recommended)

Start the interface:

```bash
streamlit run app.py
```

Interface overview:
- Home tab: analyze a single stock, select strategy, tune parameters, run backtest and view equity curve and trade table.
- LeaderBoard tab: run batch backtests across multiple stocks and strategies, view ranked results (by Sharpe or other metric), and export CSV.
- Export: save trade logs and summary reports to `reports/`.


### CLI mode

Run a single backtest via CLI:

```bash
python main.py
# follow interactive prompts: symbol, strategy, start/end dates
```

Outputs:
- Markdown report saved to `reports/`
- Trade log CSV saved to `reports/trades_<symbol>_<strategy>.csv`


## 10. LeaderBoard & batch backtests

The LeaderBoard tab provides an easy way to evaluate strategy performance across a universe of symbols. It does the following:
- Iterates over the stock list and selected strategies
- Uses cached OHLCV data when available to avoid re-downloading
- Produces summary metrics and ranks symbols by a chosen metric (default: Sharpe)
- Allows export of the leaderboard as CSV for downstream analysis

Performance notes:
- Running the full universe × strategies can be time-consuming the first time (network-bound). Subsequent runs are much faster thanks to caching.


## 11. Configuration

Defaults are set in `src/data_loader.py` and `src/backtester.py`. Common knobs:
- DATA_DIR (path to cached CSVs in data/)
- START, END (default lookback period)
- INITIAL_CAPITAL (default ₹100,000)
- COMMISSION_BUY / COMMISSION_SELL (default 0.001 = 0.1%)

For reproducible results, pin the start and end dates when running backtests and commit parameter files or the generated reports.


## 12. Outputs & example report

Reports are generated into `reports/` as both Markdown and CSV. Example report snippet:

```
# Backtest Report

Strategy         : SMA STRATEGY
Stock            : TCS
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

Trade CSV schema example: entry_date, exit_date, entry_price, exit_price, quantity, pnl, cumulative_equity


## 13. Troubleshooting

- "No data returned for 'X'": verify the symbol exists on Yahoo Finance or update the STOCKS mapping in `src/data_loader.py`.
- "Not enough data to calculate 200-day SMA": expand the START date or reduce window sizes.
- "KeyError: Unknown symbol": ensure the symbol is defined in STOCKS or pass a correct ticker.
- "Network error fetching data": confirm internet access and yfinance availability.
- Streamlit cache not updating: run `streamlit cache clear` or restart the app.


## 14. Testing & development notes

- Unit tests are in `tests/`. Run them with `pytest`.
- To add tests for a new strategy, place test inputs (small DataFrame) and assert expected entries/exits and metrics.
- Follow the existing strategy API contract when adding new strategy functions.


## 15. Roadmap

Planned enhancements:
- Multiple position support and position sizing rules
- Shorting support and margin/leverage models
- Slippage models and more realistic execution simulation
- Parameter optimization (grid search) and walk-forward testing
- Additional indicators (MACD, Bollinger Bands) and ML-based strategies
- Real-time trading connectivity


## 16. Contribution & license

This project is open-source. Contributions are welcome — please open an issue or submit a pull request. When contributing:
- Add or update tests for new functionality
- Keep the API contract for strategies clear and documented
- Ensure reproducible default parameters in configs or examples

Disclaimer: This framework is for educational and research purposes only. Past performance is not indicative of future results. Consult a financial professional before trading.

---

**Last Updated**: June 16 2026
**Version**: 2.2
