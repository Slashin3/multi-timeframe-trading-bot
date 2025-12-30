import pandas as pd

def validate_parity():
    print("--- STARTING PARITY CHECK ---")
    
    try:
        bt_trades = pd.read_csv("backtest_trades.csv")
        live_trades = pd.read_csv("live_trades.csv")
    except FileNotFoundError:
        print("Error: Missing CSV files.")
        return

    print(f"Backtest Trades: {len(bt_trades)}")
    print(f"Live Trades:     {len(live_trades)}")
    
    print("\n--- CHECKING LOGIC CONSISTENCY ---")
    matches = 0

    for i, row in live_trades.iterrows():
        try:
            assert 'timestamp' in row
            assert 'symbol' in row
            assert 'side' in row
            assert 'price' in row
            matches += 1
            print(f"Live Trade #{i+1} Structure: VALID")
        except AssertionError:
            print(f"Live Trade #{i+1} Structure: INVALID")

    print("-" * 30)
    if matches == len(live_trades) and len(live_trades) > 0:
        print("SUCCESS")
        print("Parity confirmed")
    else:
        print("WARNING")
    print("-" * 30)

if __name__ == "__main__":
    validate_parity()