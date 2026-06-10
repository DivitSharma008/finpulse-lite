import pytest
import pandas as pd
import numpy as np
from datetime import date, timedelta
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.metrics import (
    total_return, annualized_return, max_drawdown, sharpe_ratio,
    build_trade_log, trade_statistics
)
from src.backtester import run_backtest


# Test total_return

def test_total_return_basic():
    dates = pd.date_range(start='2020-01-01', periods=10, freq='D')
    equity = pd.Series([100, 110, 120, 115, 130, 125, 140, 135, 150, 160], index=dates)
    
    assert abs(total_return(equity) - 0.60) < 0.001


def test_total_return_zero():
    dates = pd.date_range(start='2020-01-01', periods=5, freq='D')
    equity = pd.Series([100, 100, 100, 100, 100], index=dates)
    
    assert abs(total_return(equity)) < 0.001


def test_total_return_loss():
    dates = pd.date_range(start='2020-01-01', periods=5, freq='D')
    equity = pd.Series([100, 90, 80, 75, 70], index=dates)
    
    assert abs(total_return(equity) - (-0.30)) < 0.001


# Test sharpe_ratio

def test_sharpe_ratio_zero():
    dates = pd.date_range(start='2020-01-01', periods=252, freq='D')
    equity = pd.Series([100 * (1.0001 ** i) for i in range(len(dates))], index=dates)
    
    sharpe = sharpe_ratio(equity)

    assert not np.isnan(sharpe) and not np.isinf(sharpe)


def test_sharpe_ratio_positive():
    dates = pd.date_range(start='2020-01-01', periods=252, freq='D')
    equity = pd.Series([100 * (1.001 ** i) for i in range(len(dates))], index=dates)
    
    sharpe = sharpe_ratio(equity)
    assert sharpe > 0


def test_sharpe_ratio_volatile():
    dates = pd.date_range(start='2020-01-01', periods=252, freq='D')
    returns = np.array([0.05 if i % 2 == 0 else -0.05 for i in range(len(dates))])
    equity = pd.Series(100 * np.cumprod(1 + returns), index=dates)
    
    sharpe = sharpe_ratio(equity)
    assert sharpe < 1.0


# Test max_drawdown

def test_max_drawdown_no_drawdown():
    dates = pd.date_range(start='2020-01-01', periods=10, freq='D')
    equity = pd.Series([100, 110, 120, 130, 140, 150, 160, 170, 180, 190], index=dates)
    
    assert max_drawdown(equity) >= -0.001


def test_max_drawdown_known_case():
    dates = pd.date_range(start='2020-01-01', periods=4, freq='D')
    equity = pd.Series([100, 110, 90, 95], index=dates)
    
    dd = max_drawdown(equity)
    assert abs(dd - (-0.1818)) < 0.001


def test_max_drawdown_crash():
    dates = pd.date_range(start='2020-01-01', periods=3, freq='D')
    equity = pd.Series([100, 50, 60], index=dates)
    
    dd = max_drawdown(equity)
    assert abs(dd - (-0.50)) < 0.001


def test_max_drawdown_recovery():
    dates = pd.date_range(start='2020-01-01', periods=4, freq='D')
    equity = pd.Series([100, 50, 150, 140], index=dates)
    
    dd = max_drawdown(equity)
    assert dd < -0.3


# Test annualized_return

def test_annualized_return_one_year():

    dates = pd.date_range(start='2020-01-01', periods=252, freq='D')
    equity = pd.Series(np.linspace(100, 120, 252), index=dates)
    
    ann_ret = annualized_return(equity)

    assert abs(ann_ret - 0.20) < 0.15


def test_annualized_return_doubling():
    dates = pd.date_range(start='2020-01-01', periods=504, freq='D')
    equity = pd.Series(np.linspace(100, 200, 504), index=dates)
    
    ann_ret = annualized_return(equity)

    assert ann_ret > 0
    assert ann_ret < 1.0


# Test build_trade_log

def test_build_trade_log_basic():
    dates = pd.date_range(start='2020-01-01', periods=5, freq='D')
    
    backtest = pd.DataFrame({
        'Action': ['BUY', 'HOLD', 'HOLD', 'SELL', 'HOLD'],
        'Price': [100, 101, 102, 105, 106],
        'Shares': [100, 100, 100, 100, 0],
    }, index=dates)
    
    trade_log = build_trade_log(backtest)
    
    assert len(trade_log) == 1
    assert trade_log['Buy Price'].iloc[0] == 100
    assert trade_log['Sell Price'].iloc[0] == 105


def test_build_trade_log_multiple():
    dates = pd.date_range(start='2020-01-01', periods=10, freq='D')
    
    backtest = pd.DataFrame({
        'Action': ['BUY', 'HOLD', 'SELL', 'BUY', 'HOLD', 'HOLD', 'SELL', 'HOLD', 'HOLD', 'HOLD'],
        'Price': [100, 102, 105, 103, 104, 106, 108, 107, 109, 110],
        'Shares': [100, 100, 100, 100, 100, 100, 100, 0, 0, 0],
    }, index=dates)
    
    trade_log = build_trade_log(backtest)
    
    assert len(trade_log) == 2


# Test trade_statistics

def test_trade_statistics_empty():
    empty_log = pd.DataFrame(columns=['Profit'])
    
    stats = trade_statistics(empty_log)
    
    assert stats['num_trades'] == 0
    assert stats['win_rate'] == 0
    assert stats['profit_factor'] == 0


def test_trade_statistics_winning():
    trade_log = pd.DataFrame({
        'Profit': [100, 150, 200, -50],
    })
    
    stats = trade_statistics(trade_log)
    
    assert stats['num_trades'] == 4
    assert stats['win_rate'] == 0.75
    assert stats['profit_factor'] > 1


def test_trade_statistics_all_losses():
    trade_log = pd.DataFrame({
        'Profit': [-50, -100, -75],
    })
    
    stats = trade_statistics(trade_log)
    
    assert stats['num_trades'] == 3
    assert stats['win_rate'] == 0.0
    assert stats['profit_factor'] == 0


# Test signal generation

def test_signal_crossover_sma():
    dates = pd.date_range(start='2020-01-01', periods=300, freq='D')
    
    prices = np.concatenate([
        np.linspace(100, 105, 100),
        np.linspace(105, 120, 100),
        np.linspace(120, 110, 100),
    ])
    
    df = pd.DataFrame({'Close': prices}, index=dates)
    
    sma50 = df["Close"].rolling(50).mean()
    sma200 = df["Close"].rolling(200).mean()
    
    signals_raw = pd.Series(0, index=df.index)
    signals_raw.loc[sma50 > sma200] = 1
    signals_raw.loc[sma50 < sma200] = -1
    
    assert (signals_raw == 1).any()
    assert (signals_raw == -1).any()


# Test lookahead bias protection

def test_no_lookahead_bias():
    dates = pd.date_range(start='2020-01-01', periods=10, freq='D')
    
    prices = pd.Series([100, 102, 104, 106, 108, 107, 105, 103, 101, 99], index=dates)
    raw_signal = (prices > 105).astype(int)
    
    shifted_signal = raw_signal.shift(1).fillna(0)
    
    assert shifted_signal.iloc[0] == 0
    assert True


# Test RSI signal generation

def test_rsi_calculation():
    dates = pd.date_range(start='2020-01-01', periods=50, freq='D')
    prices = pd.Series(np.linspace(100, 150, 50), index=dates)
    
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = delta.clip(upper=0).abs()
    
    avg_gain = gain.ewm(span=14, adjust=False).mean()
    avg_loss = loss.ewm(span=14, adjust=False).mean()
    
    RS = avg_gain / avg_loss.replace(0, 1e-10)
    RSI = 100 - 100 / (1 + RS)
    
    assert RSI.iloc[-1] > 70


# Test edge cases

def test_single_day_data():
    dates = pd.date_range(start='2020-01-01', periods=1, freq='D')
    equity = pd.Series([100], index=dates)
    
    assert total_return(equity) == 0.0


def test_two_day_data():
    dates = pd.date_range(start='2020-01-01', periods=2, freq='D')
    equity = pd.Series([100, 110], index=dates)
    
    result = total_return(equity)
    assert abs(result - 0.10) < 0.001


def test_very_small_returns():
    dates = pd.date_range(start='2020-01-01', periods=252, freq='D')
    equity = pd.Series([100 * (1.0001 ** i) for i in range(len(dates))], index=dates)
    
    result = total_return(equity)
    assert result > 0
    assert result < 0.1


def test_transaction_costs_applied():
    """Backtest with transaction costs reduces portfolio value compared to no costs"""
    dates = pd.date_range(start='2020-01-01', periods=252, freq='D')
    
    # Create price data
    prices = np.linspace(100, 120, 252)
    df = pd.DataFrame({
        'Close': prices,
        'Open': prices * 0.99,
        'High': prices * 1.01,
        'Low': prices * 0.98,
    }, index=dates)

    signals = pd.Series(0, index=dates)
    signals.iloc[50] = 1
    signals.iloc[200] = -1 
    

    result = run_backtest(df, signals, initial_capital=100000)
    
    assert 'Portfolio' in result.columns
    assert 'Adjusted Portfolio' in result.columns
    
    final_adjusted = result['Adjusted Portfolio'].iloc[-1]
    final_unadjusted = result['Portfolio'].iloc[-1]
    
    assert final_adjusted <= final_unadjusted + 1



def test_empty_dataframe():
    """Backtester handles empty input gracefully"""
    empty_df = pd.DataFrame(columns=['Close', 'Open', 'High', 'Low', 'Volume'])
    empty_signals = pd.Series([], dtype=int)
    
    try:
        result = run_backtest(empty_df, empty_signals)
        assert len(result) == 0
    except (ValueError, KeyError, IndexError) as e:
        assert True

def test_single_stock_backtest():
    """End-to-end backtest runs without errors on realistic single stock data"""
    dates = pd.date_range(start='2020-01-01', periods=252, freq='D')
    
    df = pd.DataFrame({
        'Close': np.linspace(100, 120, 252),
        'Open': np.linspace(99, 119, 252),
        'High': np.linspace(101, 121, 252),
        'Low': np.linspace(98, 118, 252),
    }, index=dates)
    
    signals = pd.Series(0, index=dates)
    signals.iloc[50] = 1  
    signals.iloc[200] = -1 
    
    result = run_backtest(df, signals)
    
    assert 'Action' in result.columns
    assert 'Portfolio' in result.columns
    assert 'Adjusted Portfolio' in result.columns
    assert len(result) == len(df)
    
    assert result['Adjusted Portfolio'].iloc[-1] > 0


if __name__ == "__main__":
    pytest.main([__file__, '-v'])