# 📈 FinPulse: Algorithmic Trading Backtester

A Python-based backtesting framework for evaluating technical trading strategies on Indian stock market data (NSE). FinPulse supports multiple trading strategies, automated performance metrics calculation, and comprehensive reporting.

## 🎯 Overview

FinPulse enables traders and analysts to:
- Download historical stock price data from Yahoo Finance
- Implement and test trading strategies (SMA, RSI)
- Backtest strategies against real historical data
- Calculate performance metrics (Sharpe ratio, drawdown, returns)
- Generate detailed trade logs and reports
- Compare strategy performance with buy-and-hold benchmark

## 📁 Project Structure

```
finpulse-lite/
├── data_loader.py          # Stock data fetching and management
├── strategies.py           # Technical analysis strategy implementations
├── backtester.py           # Backtesting engine
├── metrics.py              # Performance calculation utilities
├── reporting.py            # Report generation
├── data/                   # Historical stock data (CSV files)
├── images/                 # Equity curve charts
└── reports/                # Generated markdown reports
```

## 🏆 Supported Stocks

The framework supports 10 major Indian blue-chip stocks:
- RELIANCE (Reliance Industries)
- TCS (Tata Consultancy Services)
- INFY (Infosys)
- HDFCBANK (HDFC Bank)
- ICICIBANK (ICICI Bank)
- SBIN (State Bank of India)
- ITC (ITC Limited)
- LT (Larsen & Toubro)
- HINDUNILVR (Hindustan Unilever)
- KOTAKBANK (Kotak Mahindra Bank)

## 📊 Supported Strategies

### 1. SMA (Simple Moving Average)
Crossover strategy using 50-day and 200-day moving averages:
- **Buy Signal**: When 50-day SMA crosses above 200-day SMA
- **Sell Signal**: When 50-day SMA crosses below 200-day SMA
- **Minimum Data Required**: 200 days

### 2. RSI (Relative Strength Index)
Momentum-based strategy using the 14-period RSI:
- **Buy Signal**: RSI < 30 (oversold condition)
- **Sell Signal**: RSI > 70 (overbought condition)
- **Parameters**: Period=14, Oversold=30, Overbought=70

## 🚀 Installation

### Requirements
- Python 3.7+
- pandas
- numpy
- yfinance
- matplotlib

### Setup

```bash
# Clone or download the project
cd finpulse-lite

# Install dependencies
pip install pandas numpy yfinance matplotlib

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 💡 Usage

### 1. Download Stock Data

```bash
python data_loader.py
# Enter symbol: TCS.NS
# Output: [✓] TCS - 1260 rows saved
```

### 2. Generate Trading Signals

```bash
python strategies.py
# Enter symbol: TCS.NS
# Enter the strategy to be used: SMA
# [✓] SMA Signals generated
```

### 3. Run Backtest

```bash
python backtester.py
# Enter symbol: TCS.NS
# Enter the strategy to be used: SMA
# [✓] Backtest completed
# Final Portfolio: ₹ 156,234.50
```

Generates:
- Equity curve visualization comparing strategy vs buy-and-hold
- Portfolio performance data with transaction details

### 4. Calculate Performance Metrics

```bash
python metrics.py
# Enter symbol: TCS.NS
# Enter the strategy to be used: SMA
```

**Output includes:**
- Total Return
- Annualized Return
- Sharpe Ratio (risk-adjusted returns)
- Maximum Drawdown
- Win Rate
- Profit Factor
- Detailed trade log

### 5. Generate Report

```bash
python reporting.py
# Enter symbol: TCS.NS
# Enter the strategy to be used: SMA
# [✓] Report saved: reports/TCS_SMA_report.md
```

Generates a markdown report with all key metrics and period details.

## 📊 Key Metrics Explained

| Metric | Description | Interpretation |
|--------|-------------|-----------------|
| **Total Return** | Overall profit/loss percentage | Higher is better |
| **Annualized Return** | Yearly average return | Higher is better |
| **Sharpe Ratio** | Risk-adjusted return (default risk-free rate: 6.5%) | Higher is better (>1 is good) |
| **Max Drawdown** | Largest peak-to-trough decline | Closer to 0% is better |
| **Win Rate** | Percentage of profitable trades | Higher is better (>50% is good) |
| **Profit Factor** | Ratio of gross profit to gross loss | Higher is better (>1 is profitable) |

## ⚙️ Backtesting Parameters

- **Initial Capital**: ₹100,000 (configurable)
- **Commission**: 0.1% on buy orders, 0.1% on sell orders
- **Data Period**: 5 years of historical data (configurable)
- **Trading Logic**: Single position at a time (all-in/all-out)

## 📂 Output Files

### Generated Data
- `data/` - CSV files with OHLCV data
- `images/` - Equity curve charts (PNG)
- `reports/` - Performance reports (Markdown)

### Example Report Output
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

## 🏗️ Architecture

```
Data Flow:
  Yahoo Finance
       ↓
  data_loader.py → CSV files
       ↓
  strategies.py → Trading signals
       ↓
  backtester.py → Transaction log
       ↓
  metrics.py ← ← ← → reporting.py
       ↓
  Performance metrics & reports
```

## ⚠️ Limitations & Assumptions

1. **No slippage** beyond fixed commission rates
2. **Single position trading** - either fully invested or fully in cash
3. **No shorting** - only long positions
4. **Historical data only** - backtesting mode
5. **Market hours execution** - trades execute at closing price
6. **Commission fixed at 0.1%** - doesn't vary by broker

## ⚙️ Configuration

Edit these variables in `data_loader.py` to customize:

```python
DATA_DIR = "./data"  # Data storage location (cross-platform)
START = date.today() - timedelta(days=5*365)  # Lookback period
END = date.today()  # End date
STOCKS = {...}  # Supported stock symbols
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `No data returned for 'X'` | Symbol may be incorrect or delisted |
| `Not enough data to calculate 200-day SMA` | Download more historical data |
| `KeyError: Unknown symbol` | Check if symbol is in STOCKS dictionary |
| `Network error fetching data` | Check internet connection and yfinance status |

## ⚡ Performance Tips

- Use RSI strategy for faster backtests (fewer days required)
- Cache downloaded data to avoid repeated API calls
- Run backtests on multiple strategies to find optimal parameters
- Test on different time periods to validate robustness

## 🚀 Future Enhancements

- [ ] Multiple position support
- [ ] Shorting strategies
- [ ] Parameter optimization (grid search)
- [ ] Additional technical indicators (MACD, Bollinger Bands)
- [ ] Risk management (stop-loss, position sizing)
- [ ] Real-time trading integration
- [ ] Web dashboard for visualization
- [ ] Machine learning strategy generation

## ⚖️ Disclaimer

This backtesting framework is for educational and research purposes only. Past performance does not guarantee future results. Always conduct thorough due diligence and consult with a financial advisor before trading with real capital.

---

**Last Updated**: June 2026  
**Version**: 2.1
