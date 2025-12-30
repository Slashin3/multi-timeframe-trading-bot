# multi-timeframe-trading-bot

A modular, event-driven algorithmic trading engine built for the Binance ecosystem. This system features a unified logic core that ensures strict parity between historical backtesting and live execution.

## 🚀 Key Features

* **Unified Strategy Core:** The `StrategyLogic` class is decoupled from execution, allowing the exact same code to drive both the Backtester (Pandas) and the Live Trader (Binance API).
* **Multi-Timeframe Analysis:** Synthesizes market data from different intervals (e.g., 1m Entry signals filtered by 1h Trend direction).
* **Resilient Execution:** engineered with `recvWindow` handling, timestamp synchronization, and automatic error recovery for network instability.
* **Audit Logging:** Real-time CSV logging of all trade executions for performance analysis.

## 🛠️ Technical Architecture

* `live_trader.py`: The main execution engine handling API connectivity, order management, and logging.
* `strategy.py`: Contains the signal generation logic and configuration.
* `backtest_runner.py`: Historical simulation wrapper using `backtesting.py`.
* `data_downloader.py`: Utility for fetching OHLCV data from Binance.

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/multi-timeframe-trading-bot.git](https://github.com/YOUR_USERNAME/multi-timeframe-trading-bot.git)
    cd multi-timeframe-trading-bot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ⚡ Usage

### 1. Run Backtest
Verify the strategy performance on historical data.
```bash
python backtest_runner.py

Output: backtest_trades.csv

2. Run Live Trader
Connects to Binance Testnet.

Security Note: The system will prompt you for API keys at runtime. Do not hardcode keys in the script.

Bash

python live_trader.py
Output: live_trades.csv

⚠️ Disclaimer
This software is for educational purposes only. Do not risk capital you cannot afford to lose.


---

### **Final File Structure Checklist**

Before you run `git init`, your folder should look exactly like this:

1.  `live_trader.py` (The clean version I just gave you)
2.  `strategy.py` (With the logic and config)
3.  `backtest_runner.py` (The simulation script)
4.  `README.md` (The text above)
5.  `requirements.txt` (The list of libraries)
6.  `.gitignore` (Important! Containing `__pycache__` and `.env`)

**Do NOT include:**
* `BTCUSDT_1m.csv` (Too big for GitHub)
* Any file with your real API keys inside.

**You are ready to push.** Go ahead and initialize the repo!
