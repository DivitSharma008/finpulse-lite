# Day 2 — Backtesting Engine

- Built `backtest.py` with a `run_backtest()` function that tracks portfolio value at the end of each trading day.
- Used the `signals` Series from `strategy_sma.py` to drive buy and sell decisions.
- Initially attempted a vectorised approach but found it unreliable for stateful logic (e.g. tracking whether shares are held). Switched to a row-by-row loop which correctly handles all cases.
