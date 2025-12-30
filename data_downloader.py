import requests
import pandas as pd
import datetime

def fetch_binance_data(symbol, interval, limit=1000):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    
    print(f"Downloading {interval} data for {symbol}...")
    response = requests.get(url, params=params)
    data = response.json()
    
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume", 
        "close_time", "quote_asset_volume", "number_of_trades", 
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    
    df = df.astype(float)
    
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    
    # Set index
    df.set_index("timestamp", inplace=True)
    
    return df

if __name__ == "__main__":
    df_15m = fetch_binance_data("BTCUSDT", "1m", limit=1000)
    df_15m.to_csv("BTCUSDT_1m.csv")
    print("Saved BTCUSDT_1m.csv")

    df_1h = fetch_binance_data("BTCUSDT", "1h", limit=1000)
    df_1h.to_csv("BTCUSDT_1h.csv")
    print("Saved BTCUSDT_1h.csv")
    
    print("\nData download complete! You can now run backtest_runner.py")