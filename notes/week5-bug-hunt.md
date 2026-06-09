# Debugging and removing Lookahead Bias

- There are hardcoded file paths which wont work on another system
- Division by Zero error in generate_rsi_signals in strategies.py
- Error Handling is missing in backtester.py while reading the CSV data files
- Buffer not taken for the RSI exponential MA to be statbilized, resulting in unreliable signals
