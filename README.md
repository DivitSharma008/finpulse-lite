# FinPulse Lite

A Python-based stock market analysis and backtesting framework that analyzes historical stock data, generates trading signals using the SMA Crossover strategy, and evaluates trading performance through comprehensive backtesting.

## 📋 Overview

FinPulse Lite provides tools to:
- **Download** historical stock data for 10 major Indian stocks
- **Visualize** price movements with moving averages (50-day and 200-day SMA)
- **Backtest** trading strategies (SMA Crossover) with realistic brokerage costs
- **Generate** detailed equity curves and performance reports
- **Compare** trading strategies (e.g., "Buy & Hold" vs. SMA Crossover)

## 🎯 Key Features

- **Multi-Stock Analysis**: Analyze 10 major Indian stocks (RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, ITC, SBIN, LT, HINDUNILVR, KOTAKBANK)
- **SMA Crossover Strategy**: Implements 50-day and 200-day moving average crossover signals
- **Realistic Backtesting**: Includes brokerage costs (~0.1% per trade) in portfolio calculations
- **Visual Charts**: Generates high-quality charts showing closing prices and moving averages
- **Equity Curves**: Plots portfolio performance over time to compare strategies
- **Trade Logging**: Detailed logging of all trades executed during backtesting

## 📦 Installation

### Prerequisites
- Python 3.8 or higher

### Setup
1. Clone the repository:
```bash
git clone https://github.com/DivitSharma008/finpulse-lite.git
cd finpulse-lite
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies
- **yfinance**: Fetch historical stock data from Yahoo Finance
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Visualization and charting

## 🚀 Quick Start

### Step 1: Download Stock Data
Run the data loader to fetch historical stock data (stored as CSV files):
```bash
python -m src.data_loader
```
This creates CSV files in the `data/` directory with historical price data for each stock.

### Step 2: Generate Charts
Visualize closing prices and moving averages for all stocks:
```bash
python plot_stock.py
```
Charts are saved to the `images/` folder showing:
- Closing price line
- 50-day moving average
- 200-day moving average

**Example Output:**
![INFY Chart](https://github.com/user-attachments/assets/25215e19-76d5-468e-8f9b-fcf067f35033)

### Step 3: Run Backtests
Execute the full backtesting pipeline for a specific stock:
```bash
python main.py
```
When prompted, enter a stock symbol (e.g., `RELIANCE`, `INFY`, `TCS`):
```
Enter symbol: RELIANCE
```

The pipeline will:
1. Load historical data for the stock
2. Generate SMA crossover trading signals
3. Run backtesting with initial capital of ₹100,000
4. Calculate performance metrics
5. Generate equity curve visualization

**Example Equity Curve:**
![RELIANCE Backtest](https://github.com/user-attachments/assets/e8e7bc2b-6214-4534-9065-eaaa15378bd4)

## 📁 Project Structure

```
finpulse-lite/
├── main.py                 # Main pipeline orchestrator
├── plot_stock.py           # Chart generation script
├── requirements.txt        # Python dependencies
├── src/                    # Core modules
│   ├── data_loader.py     # Fetch and store stock data
│   ├── strategies.py      # Trading strategy implementations
│   ├── backtester.py      # Backtesting engine
│   ├── metrics.py         # Performance metrics calculation
│   └── reporting.py       # Report generation
├── data/                   # Historical stock data (CSV files)
├── images/                 # Generated charts
├── reports/                # Generated reports
├── notes/                  # Project notes and documentation
└── README.md              # This file
```

## 🎓 Trading Strategy

### SMA Crossover Strategy
The SMA (Simple Moving Average) Crossover strategy uses two moving averages:
- **50-day SMA**: Short-term trend indicator
- **200-day SMA**: Long-term trend indicator

**Buy Signal**: When the 50-day MA crosses above the 200-day MA (bullish)
**Sell Signal**: When the 50-day MA crosses below the 200-day MA (bearish)

### Backtesting Parameters
- **Initial Capital**: ₹100,000
- **Brokerage Cost**: 0.1% per trade
- **Position**: Single stock (all capital deployed on buy signals)

### Key Finding
Analysis of RELIANCE stock revealed that the **"Buy & Hold" strategy** outperformed the SMA Crossover strategy, suggesting that brokerage costs and whipsaw trades can diminish returns compared to a simple long-term hold approach.

## 💡 Usage Examples

### Analyze a Specific Stock
```bash
python main.py
# Enter: INFY
```

### Generate All Stock Charts
```bash
python plot_stock.py
```

### Check Stock Data
```python
import pandas as pd

# Load stock data
df = pd.read_csv("data/RELIANCE.csv", index_col="Date", parse_dates=True)
print(df.head())
print(df.describe())
```

## 📊 Output Files

The project generates:
- **CSV Files** (`data/` folder): Historical stock data with OHLC values
- **Chart Images** (`images/` folder): PNG files showing price and moving averages
- **Equity Curves** (`reports/` folder): Performance plots for backtested strategies
- **Trade Logs**: Detailed transaction history during backtesting

## 🔍 How It Works

1. **Data Ingestion**: Historical stock data is downloaded via yfinance
2. **Signal Generation**: Trading signals are generated based on moving average crossovers
3. **Backtesting**: Portfolio is simulated through historical data with realistic costs
4. **Performance Analysis**: Equity curves and metrics are calculated
5. **Visualization**: Results are displayed as charts and reports

## 🛠️ Configuration

Edit the following in relevant files:

**In `plot_stock.py`:**
```python
DATA_DIR   = r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\data"
IMAGES_DIR = r"C:\Users\DELL\OneDrive\Desktop\finpulse-lite\images"
```

**In `main.py` (backtesting):**
```python
backtest = run_backtest(df, signals, initial_capital=100000)
```

## 📝 Supported Stocks

The project currently analyzes these major Indian companies:
- RELIANCE - Reliance Industries
- TCS - Tata Consultancy Services
- INFY - Infosys Limited
- HDFCBANK - HDFC Bank
- ICICIBANK - ICICI Bank
- ITC - ITC Limited
- SBIN - State Bank of India
- LT - Larsen & Toubro
- HINDUNILVR - Hindustan Unilever
- KOTAKBANK - Kotak Mahindra Bank


**Last Updated**: June 4 2026
