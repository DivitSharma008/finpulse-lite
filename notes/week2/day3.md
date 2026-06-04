# Day 3 — Transaction Costs

- Added a standard 0.1% transaction cost to `run_backtest()`, applied on both buy (slippage) and sell (brokerage).
- Compared raw vs adjusted portfolio values and observed a difference of ₹116 in the final portfolio — confirming that even small costs compound over many trades.
