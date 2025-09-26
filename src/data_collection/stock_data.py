import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional

class StockDataCollector:
    @staticmethod
    def get_stock_data(ticker: str,
                       start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> pd.DataFrame:
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(start = start_date, end = end_date)
            
            df['Returns'] = df['Close'] - df['Open']
            df['Volume_Ratio'] = df['Volume'] / df['Volume'].rolling(20).mean()
            df['Volatility'] = df['Returns'].rolling(5).std()
            
            df['Price_Change'] = df['Close'] - df['Open']
            df['Price_Change_Percent'] = (df['Price_Change'] / df['Open']) * 100
            
            return df
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return pd.DataFrame()