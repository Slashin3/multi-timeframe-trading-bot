from backtesting import Backtest, Strategy
import pandas as pd
from strategy import StrategyLogic

# --- CONFIGURATION ---
DATA_FILE_15M = "BTCUSDT_1m.csv"
DATA_FILE_1H = "BTCUSDT_1h.csv"

class MyBacktestStrategy(Strategy):

    logic = StrategyLogic()

    def init(self):
        self.fast_ma = self.I(lambda: self.data.fast_ma, name='FastMA')
        self.slow_ma = self.I(lambda: self.data.slow_ma, name='SlowMA')
        self.trend_ma = self.I(lambda: self.data.trend_ma_1h, name='TrendMA_1H')

    def next(self):
        row = {
            'Close': self.data.Close[-1],
            'fast_ma': self.fast_ma[-1],
            'slow_ma': self.slow_ma[-1],
            'trend_ma_1h': self.trend_ma[-1]
        }

        signal = self.logic.calculate_entry_exit(row)
        
        #EXECUTION
        if signal == 1:
            if not self.position.is_long:
                self.position.close()
                self.buy()
                
        elif signal == -1:
            if not self.position.is_short:
                self.position.close()
                self.sell()

def run_backtest():
    print("Loading data...")
    try:
        df_15m = pd.read_csv(DATA_FILE_15M, parse_dates=True, index_col='timestamp')
        df_1h = pd.read_csv(DATA_FILE_1H, parse_dates=True, index_col='timestamp')
    except FileNotFoundError:
        print("Error: CSV files not found. Please run data_downloader.py first.")
        return

    df_15m.columns = [x.capitalize() for x in df_15m.columns] # close -> Close
    df_1h.columns = [x.capitalize() for x in df_1h.columns]   # close -> Close

    logic = StrategyLogic()
    print("Aligning Multi-Timeframe Data...")
    
    merged_data = logic.prepare_data(df_15m, df_1h)
    
    if len(merged_data) == 0:
        print("Error: No data left after merging. Check your timestamps.")
        return
    merged_data.rename(columns={
        'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume'
    }, inplace=True)

    print("Running Backtest...")
    bt = Backtest(merged_data, MyBacktestStrategy, cash=1000000, commission=.002)
    stats = bt.run()
    
    trades = stats['_trades']
    trades.to_csv("backtest_trades.csv")
    
    print("\n--- Backtest Complete ---")
    print(stats)
    print("Trades saved to backtest_trades.csv")

if __name__ == "__main__":
    run_backtest()