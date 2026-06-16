# 📈 FinPulse: Algorithmic Trading Backtester

A Python-based backtesting framework for evaluating technical trading strategies on Indian stock market data (NSE). FinPulse supports multiple trading strategies with both a CLI and interactive Streamlit web interface for analysis and visualization.

## 🎯 Overview

FinPulse enables traders and analysts to:
- Download historical stock price data from Yahoo Finance
- Implement and test trading strategies (SMA, RSI)
- Backtest strategies against real historical data
- Calculate performance metrics (Sharpe ratio, drawdown, returns)
- Generate detailed trade logs and reports
- Compare strategy performance with buy-and-hold benchmark
- **Run interactive backtests via Streamlit web dashboard**
- **Compare multiple stocks and strategies simultaneously with leaderboard**

## 📁 Project Structure

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
├── data/                   # Historical stock data (CSV files)
├── reports/                # Generated markdown reports
├── tests/                  # Unit tests
└── notes/                  # Development notes
```

## 🏆 Supported Stocks

The framework supports multiple Indian blue-chip stocks:
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
- And more...

## 📊 Supported Strategies

### 1. SMA (Simple Moving Average)
Crossover strategy using 50-day and 200-day moving averages:
- **Buy Signal**: When 50-day SMA crosses above 200-day SMA
- **Sell Signal**: When 50-day SMA crosses below 200-day SMA
- **Minimum Data Required**: 200 days
- **Customizable**: Adjust fast/slow windows via UI

### 2. RSI (Relative Strength Index)
Momentum-based strategy using the 14-period RSI:
- **Buy Signal**: RSI < 30 (oversold condition)
- **Sell Signal**: RSI > 70 (overbought condition)
- **Parameters**: Period, Oversold, Overbought thresholds (all adjustable)

## 🚀 Installation

### Requirements
- Python 3.7+
- pandas
- numpy
- yfinance
- matplotlib
- plotly
- streamlit

### Setup

```bash
# Clone or download the project
git clone https://github.com/DivitSharma008/finpulse-lite.git
cd finpulse-lite

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 💡 Usage

### Option 1: Interactive Web Dashboard (Recommended)

```bash
streamlit run app.py
```

**Features:**
- Real-time strategy parameter tuning
- Interactive equity curve charts
- Strategy vs Buy & Hold comparison
- Leaderboard showing performance across all stocks
- Export results to CSV

**Interface:**
- **Home Tab**: Single stock analysis with customizable strategies
- **LeaderBoard Tab**: Run all backtests and compare performance

### Option 2: CLI Mode

```bash
python main.py
# Enter symbol: TCS
# Enter the strategy to be used: SMA
```

**Output includes:**
- Generated markdown reports
- Performance metrics
- Detailed trade log

### Example Workflow

**Step 1: Launch Dashboard**
```bash
streamlit run app.py
```

**Step 2: Select Stock**
- Choose from dropdown list of supported stocks

**Step 3: Configure Strategy**
- Select strategy (SMA or RSI)
- Adjust parameters (window sizes, thresholds)

**Step 4: Run Backtest**
- View equity curve
- Compare against buy-and-hold
- Analyze trade statistics

**Step 5: Compare Performance**
- Navigate to LeaderBoard
- Run all backtests for comparison
- Filter by strategy
- Export results

## 📊 Key Metrics Explained

| Metric | Description | Interpretation |
|--------|-------------|-----------------|
| **Sharpe Ratio** | Risk-adjusted return (default risk-free rate: 6.5%) | Higher is better (>1 is good) |
| **Total Return** | Overall profit/loss percentage | Higher is better |
| **Annualized Return** | Yearly average return | Higher is better |
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
- `reports/` - Performance reports (Markdown)

### Example Report Output
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

## 🏗️ Architecture

```
Data Flow:
  Yahoo Finance
       ↓
  data_loader.py → CSV files (cached)
       ↓
  strategies.py → Trading signals
       ↓
  backtester.py → Transaction log
       ↓
  metrics.py ← ← ← → reporting.py
       ↓
  Performance metrics & reports
       ↓
   (Web UI via Streamlit or CLI)
```

## 🎯 Streamlit Features

### Home Tab
- Select and visualize individual stock prices
- Choose strategy and customize parameters in real-time
- Run single backtests with detailed results
- View equity curves and trade statistics
- Compare strategy performance vs buy-and-hold

### LeaderBoard Tab
- **Run All Backtests**: Execute all 50+ stocks × 2 strategies
- **Leaderboard Display**: Ranked by Sharpe ratio
- **Top/Bottom Performers**: See best and worst performing strategies
- **Summary Statistics**: Aggregate metrics across all backtests
- **Export Results**: Download leaderboard as CSV
- **Caching**: Subsequent runs are much faster due to cached data

## ⚠️ Limitations & Assumptions

1. **No slippage** beyond fixed commission rates
2. **Single position trading** - either fully invested or fully in cash
3. **No shorting** - only long positions
4. **Historical data only** - backtesting mode
5. **Market hours execution** - trades execute at closing price
6. **Commission fixed at 0.1%** - doesn't vary by broker

## ⚙️ Configuration

Edit these variables in `src/data_loader.py` to customize:

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
| `Streamlit cache not updating` | Clear cache: `streamlit cache clear` |

## ⚡ Performance Tips

- Use RSI strategy for faster backtests (fewer days required)
- Streamlit caches results - subsequent runs are very fast
- LeaderBoard runs all backtests efficiently with progress tracking
- Run backtests on multiple strategies to find optimal parameters
- Test on different time periods to validate robustness

## 🚀 Future Enhancements

- [ ] Multiple position support
- [ ] Shorting strategies
- [ ] Parameter optimization (grid search)
- [ ] Additional technical indicators (MACD, Bollinger Bands)
- [ ] Risk management (stop-loss, position sizing)
- [ ] Real-time trading integration
- [ ] Advanced portfolio analysis charts
- [ ] Machine learning strategy generation
- [ ] Export to TradingView

## ⚖️ Disclaimer

This backtesting framework is for educational and research purposes only. Past performance does not guarantee future results. Always conduct thorough due diligence and consult with a financial advisor before trading. The authors assume no responsibility for trading decisions made using this software.

## 📝 License

This project is open-source. Feel free to use, modify, and distribute as needed.

---

**Last Updated**: June 2026  
**Version**: 2.2
