import pandas as pd
import numpy as np

class StrategyConfig:
    TIMEFRAME_TRADING = '15m'
    TIMEFRAME_FILTER = '1h'
    
    FAST_MA_PERIOD = 5   
    SLOW_MA_PERIOD = 15  
    TREND_MA_PERIOD = 20 
    
    STOP_LOSS_PCT = 0.02 
    TAKE_PROFIT_PCT = 0.04 

class StrategyLogic:
    def __init__(self):
        self.config = StrategyConfig()

    def calculate_indicators(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        df = df.copy()
        
        df['Close'] = pd.to_numeric(df['Close'])
        
        if timeframe == self.config.TIMEFRAME_TRADING: # 15m
            df['fast_ma'] = df['Close'].rolling(window=self.config.FAST_MA_PERIOD).mean()
            df['slow_ma'] = df['Close'].rolling(window=self.config.SLOW_MA_PERIOD).mean()
            
        elif timeframe == self.config.TIMEFRAME_FILTER: # 1h
            df['trend_ma'] = df['Close'].rolling(window=self.config.TREND_MA_PERIOD).mean()
            
        return df

    def prepare_data(self, df_trading: pd.DataFrame, df_filter: pd.DataFrame) -> pd.DataFrame:

        df_trading = self.calculate_indicators(df_trading, self.config.TIMEFRAME_TRADING)
        df_filter = self.calculate_indicators(df_filter, self.config.TIMEFRAME_FILTER)

        df_filter = df_filter.add_suffix('_1h')

        merged_df = pd.merge_asof(
            df_trading.sort_index(), 
            df_filter.sort_index(), 
            left_index=True, 
            right_index=True, 
            direction='backward'
        )
        
        merged_df.dropna(inplace=True)
        
        return merged_df

    def calculate_entry_exit(self, row) -> int:

        fast_ma = row['fast_ma']
        slow_ma = row['slow_ma']

        crossover_bullish = fast_ma > slow_ma
        crossover_bearish = fast_ma < slow_ma
        

        if crossover_bullish:
            return 1
            
        elif crossover_bearish:
            return -1
            
        return 0