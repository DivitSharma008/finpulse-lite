# Day 3 — RSI Strategy

- Implemented the RSI (Relative Strength Index) strategy in `strategies.py`.
- The strategy uses a 14-day RSI with the following rules:
  - RSI < 30 (oversold) → **BUY**
  - RSI > 70 (overbought) → **SELL**
- Used `delta.clip()` for clean gain/loss separation and `.ewm(alpha=1/period)` for the exponential moving average — avoiding sign errors present in naive implementations.
