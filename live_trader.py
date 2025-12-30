import time
import os
import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
from strategy import StrategyLogic, StrategyConfig

# --- CONFIGURATION ---
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

if not API_KEY or not API_SECRET:
    print("\n--- API Credentials Required ---")
    API_KEY = input("Enter Binance Testnet API Key: ").strip()
    API_SECRET = input("Enter Binance Testnet Secret Key: ").strip()

SYMBOL = "BTCUSDT"
QUANTITY = 0.001 

class LiveTrader:
    def __init__(self, api_key, api_secret, symbol):
        print(f"Connecting to Binance Testnet for {symbol}...")
        self.client = Client(api_key, api_secret, testnet=True)
        self.symbol = symbol
        self.logic = StrategyLogic()
        self.config = StrategyConfig()
        
        # Setup Logging
        self.trade_log_file = "live_trades.csv"
        try:
            with open(self.trade_log_file, 'w') as f:
                f.write("timestamp,symbol,side,price,quantity,status\n")
        except FileExistsError:
            pass

    def get_data(self):
        # Helper to get dataframe
        def fetch_klines(interval, limit=100):
            try:
                klines = self.client.get_klines(symbol=self.symbol, interval=interval, limit=limit)
            except Exception as e:
                print(f"Error fetching data: {e}")
                return pd.DataFrame() 

            df = pd.DataFrame(klines, columns=[
                "Open Time", "Open", "High", "Low", "Close", "Volume", 
                "Close Time", "QAV", "NAT", "TBBAV", "TBQAV", "Ignore"
            ])
            df["Close"] = pd.to_numeric(df["Close"])
            df["Open Time"] = pd.to_datetime(df["Open Time"], unit='ms')
            df.set_index("Open Time", inplace=True)
            return df[['Close']]

        df_1m = fetch_klines(self.config.TIMEFRAME_TRADING)
        df_1h = fetch_klines(self.config.TIMEFRAME_FILTER)
        return df_1m, df_1h

    def execute_trade(self, signal, current_price):
        side = "BUY" if signal == 1 else "SELL"
        print(f"\n!!!!!! SIGNAL DETECTED: {side} @ {current_price} !!!!!!")
        
        status = "FILLED"
        
        try:
            order = self.client.create_order(
                symbol=self.symbol,
                side=side,
                type='MARKET',
                quantity=QUANTITY,
                recvWindow=10000 #binance testnet is very laggy
            )
            print(f"Order Executed Successfully! Order ID: {order['orderId']}")
            
        except BinanceAPIException as e: 
            print(f"Binance Error: {e.message}")
            print(">>> SWITCHING TO PAPER TRADE MODE (Saving to CSV anyway) <<<")
            status = "PAPER_TRADE_ERROR"
        except Exception as e:
            print(f"Unknown Error: {e}")
            status = "ERROR"

        #CSV
        with open(self.trade_log_file, 'a') as f:
            f.write(f"{pd.Timestamp.now()},{self.symbol},{side},{current_price},{QUANTITY},{status}\n")
        print(f"Trade saved to live_trades.csv (Status: {status})")

    def run(self):
        print(f"System Running. Waiting for trades...")
        while True:
            try:
                df_1m, df_1h = self.get_data()
                if df_1m.empty: 
                    time.sleep(5)
                    continue
                
                merged_data = self.logic.prepare_data(df_1m, df_1h)
                if merged_data.empty: 
                    time.sleep(5)
                    continue

                last_row = merged_data.iloc[-1]
                signal = self.logic.calculate_entry_exit(last_row)
                current_price = last_row['Close']
                
                print(f"\rTime: {last_row.name} | Price: {current_price:.2f} | Signal: {signal}", end="")
                
                if signal != 0:
                    self.execute_trade(signal, current_price)
                    print("\nPausing for 60 seconds...")
                    time.sleep(60) 
                
                time.sleep(5) 
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\nError: {e}")
                time.sleep(5)

if __name__ == "__main__":
    trader = LiveTrader(API_KEY, API_SECRET, SYMBOL)
    trader.run()