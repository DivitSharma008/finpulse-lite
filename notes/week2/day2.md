I created backtest.py where in I used a run_backtest function to calculate portfolio value at the end of each day
I used the signals Series from the strategy_sma.py file to determine buy and sell signals.
I faced multiple problems while using a vectorised approach to find buy and sell signals.
Instead an approach of using loops to traverse the dataframe is ideal as it traverses the entire dataframe.

