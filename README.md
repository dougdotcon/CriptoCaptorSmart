# 🔥 CryptoCaptorSmart: Cyberpunk Terminal 🔥

## 🎯 Overview

A universal cryptocurrency analysis system featuring a cyberpunk-inspired terminal interface. It provides advanced technical indicators, market correlations, and real-time insights for any digital asset.

## ✨ Features

### 🎨 Futuristic Terminal Interface
- **Animated ASCII Banner** with cyberpunk art
- **Neon Color Palette** (cyan, green, yellow, magenta, red)
- **Loading Animations** with special characters
- **Styled Menus** with ASCII borders
- **Visual Feedback** for all operations

### 🚀 Universal Capabilities
- **Search any cryptocurrency** via multiple APIs
- **Complete Technical Analysis** (RSI, MACD, Bollinger Bands, etc.)
- **Correlation Analysis** between two cryptocurrencies
- **Market Cycle Identification** (bull/bear markets)
- **Pre-configured Popular Cryptocurrencies**
- **Cyberpunk Dashboard** (in development)

## 🛠️ Installation

### 1. Automatic Method (Recommended)
bash
python start_crypto_cyberpunk.py

The script will automatically check and install all necessary dependencies.

### 2. Manual Method
bash
pip install -r requirements.txt
python cyberpunk_crypto_terminal.py


### 3. Windows (Batch)
cmd
start_crypto_cyberpunk.bat


## 🎮 How to Use

### 1. Initialization
Run the launcher:
bash
python start_crypto_cyberpunk.py


### 2. Main Menu

╔═══════════════════════════════════════════════════════════════════════════╗
║                           MAIN MENU                                      ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ [1] ► SEARCH CRYPTOCURRENCIES                                            ║
║ [2] ► INDIVIDUAL ANALYSIS                                                ║
║ [3] ► COMPARATIVE ANALYSIS                                               ║
║ [4] ► CYBERPUNK DASHBOARD                                                ║
║ [5] ► POPULAR CRYPTOS                                                    ║
║ [6] ► SETTINGS                                                           ║
║ [0] ► DISCONNECT FROM SYSTEM                                             ║
╚═══════════════════════════════════════════════════════════════════════════╝


### 3. Analysis Workflow
1. **Search for a cryptocurrency** (option 1) or **select a popular one** (option 5)
2. **Run individual analysis** (option 2) for technical indicators
3. **Compare two cryptos** (option 3) for correlation analysis
4. **View the dashboard** (option 4) for interactive charts

## 📊 Available Analyses

### 🔍 Individual Analysis
- **Performance**: Total return, annualized return, volatility, Sharpe ratio
- **Technical Indicators**: RSI, MACD, Bollinger Bands, moving averages
- **Support/Resistance**: Key technical levels
- **Market Cycles**: Bull/Bear market identification

### 🔗 Comparative Analysis
- **Price Correlation**: Correlation between two cryptocurrencies
- **Return Correlation**: Correlation of returns
- **Volatility Comparison**: Compare volatility profiles
- **Performance Metrics**: Side-by-side comparison

## ⚙️ Requirements

- Python 3.8+
- Dependencies: `yfinance`, `pandas`, `numpy`, `matplotlib`, `requests`, `tabulate`

## 📝 Note

This project uses **yahoo-finance** as the primary data source. Some cryptocurrencies may have limited historical data depending on their listing date and market availability.