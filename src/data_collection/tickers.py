import re
from typing import List, Set

stock_tickers = {
    # Technology
    'AAPL': ['Apple', 'Apple Inc'],
    'MSFT': ['Microsoft', 'Microsoft Corporation'],
    'GOOGL': ['Google', 'Alphabet', 'Alphabet Inc'],
    'GOOG': ['Google', 'Alphabet', 'Alphabet Inc'],
    'AMZN': ['Amazon', 'Amazon.com'],
    'META': ['Meta', 'Facebook', 'Meta Platforms'],
    'TSLA': ['Tesla', 'Tesla Inc'],
    'NVDA': ['NVIDIA', 'Nvidia Corporation'],
    'NFLX': ['Netflix', 'Netflix Inc'],
    'ADBE': ['Adobe', 'Adobe Inc'],
    'CRM': ['Salesforce', 'Salesforce Inc'],
    'ORCL': ['Oracle', 'Oracle Corporation'],
    'IBM': ['IBM', 'International Business Machines'],
    'INTC': ['Intel', 'Intel Corporation'],
    'AMD': ['AMD', 'Advanced Micro Devices'],
    'UBER': ['Uber', 'Uber Technologies'],
    'LYFT': ['Lyft', 'Lyft Inc'],
    'SNAP': ['Snapchat', 'Snap Inc'],
    'TWTR': ['Twitter', 'Twitter Inc'],
    'SPOT': ['Spotify', 'Spotify Technology'],
    'SQ': ['Square', 'Block Inc'],
    'PYPL': ['PayPal', 'PayPal Holdings'],
    'SHOP': ['Shopify', 'Shopify Inc'],
    'ZM': ['Zoom', 'Zoom Video Communications'],
    'CRWD': ['CrowdStrike', 'CrowdStrike Holdings'],
    
    # Finance
    'JPM': ['JPMorgan Chase', 'JPMorgan', 'Chase'],
    'BAC': ['Bank of America', 'BofA'],
    'WFC': ['Wells Fargo', 'Wells Fargo & Company'],
    'GS': ['Goldman Sachs', 'Goldman Sachs Group'],
    'MS': ['Morgan Stanley'],
    'C': ['Citigroup', 'Citi', 'Citibank'],
    'V': ['Visa', 'Visa Inc'],
    'MA': ['Mastercard', 'Mastercard Inc'],
    'AXP': ['American Express', 'AmEx'],
    'BRK.A': ['Berkshire Hathaway', 'Berkshire'],
    'BRK.B': ['Berkshire Hathaway', 'Berkshire'],
    
    # Healthcare & Pharmaceuticals
    'JNJ': ['Johnson & Johnson', 'J&J'],
    'PFE': ['Pfizer', 'Pfizer Inc'],
    'UNH': ['UnitedHealth', 'UnitedHealth Group'],
    'CVS': ['CVS Health', 'CVS'],
    'ABBV': ['AbbVie', 'AbbVie Inc'],
    'LLY': ['Eli Lilly', 'Lilly'],
    'MRK': ['Merck', 'Merck & Co'],
    'BMY': ['Bristol Myers Squibb', 'BMS'],
    'GILD': ['Gilead', 'Gilead Sciences'],
    'AMGN': ['Amgen', 'Amgen Inc'],
    
    # Consumer & Retail
    'WMT': ['Walmart', 'Walmart Inc'],
    'HD': ['Home Depot', 'The Home Depot'],
    'PG': ['Procter & Gamble', 'P&G'],
    'KO': ['Coca-Cola', 'The Coca-Cola Company'],
    'PEP': ['PepsiCo', 'Pepsi'],
    'MCD': ['McDonald\'s', 'McDonald\'s Corporation'],
    'SBUX': ['Starbucks', 'Starbucks Corporation'],
    'NKE': ['Nike', 'Nike Inc'],
    'DIS': ['Disney', 'The Walt Disney Company'],
    'LOW': ['Lowe\'s', 'Lowe\'s Companies'],
    'TGT': ['Target', 'Target Corporation'],
    'COST': ['Costco', 'Costco Wholesale'],
    
    # Energy
    'XOM': ['ExxonMobil', 'Exxon Mobil'],
    'CVX': ['Chevron', 'Chevron Corporation'],
    'COP': ['ConocoPhillips'],
    'SLB': ['Schlumberger'],
    'EOG': ['EOG Resources'],
    
    # Industrial
    'BA': ['Boeing', 'The Boeing Company'],
    'CAT': ['Caterpillar', 'Caterpillar Inc'],
    'GE': ['General Electric', 'GE'],
    'MMM': ['3M', '3M Company'],
    'HON': ['Honeywell', 'Honeywell International'],
    'UPS': ['UPS', 'United Parcel Service'],
    'FDX': ['FedEx', 'FedEx Corporation'],
    
    # Telecommunications
    'VZ': ['Verizon', 'Verizon Communications'],
    'T': ['AT&T', 'AT&T Inc'],
    'TMUS': ['T-Mobile', 'T-Mobile US'],
    'CMCSA': ['Comcast', 'Comcast Corporation'],
    
    # Utilities
    'NEE': ['NextEra Energy', 'NextEra'],
    'DUK': ['Duke Energy', 'Duke Energy Corporation'],
    'SO': ['Southern Company', 'Southern'],
    'AEP': ['American Electric Power', 'AEP'],
    
    # Real Estate Investment Trusts (REITs)
    'AMT': ['American Tower', 'American Tower Corporation'],
    'PLD': ['Prologis', 'Prologis Inc'],
    'CCI': ['Crown Castle', 'Crown Castle International'],
    'EQIX': ['Equinix', 'Equinix Inc'],
    
    # Other Notable Companies
    'BABA': ['Alibaba', 'Alibaba Group'],
    'TSM': ['TSMC', 'Taiwan Semiconductor'],
    'ASML': ['ASML', 'ASML Holding'],
    'NVO': ['Novo Nordisk'],
    'TM': ['Toyota', 'Toyota Motor'],
    'BHP': ['BHP', 'BHP Group'],
    'RIO': ['Rio Tinto'],
}
        
class TickerExtractor():
    def __init__(self):
        self.name_to_ticker = {}
        for ticker, names in stock_tickers.items():
            for name in names:
                self.name_to_ticker[name.lower()] = ticker
                
        self._create_patterns()
        
    def _create_patterns(self):
        self.ticker_pattern = re.compile(r'\b[A-Z]{1, 5}(?:\.[A-Z])?\b')
        
        company_names = sorted(self.name_to_ticker.keys(), key=len, reverse=True)
        escaped_names = [re.escape(name) for name in company_names]
        
        self.company_pattern = re.compile(
            r'\b(?:' + '|'.join(escaped_names) + r')\b', 
            re.IGNORECASE
        )
        
    def extract_tickers(self, text: str) -> List[str]:
        if not text:
            return []
        
        found_tickers = set()
        
        ticker_matches = self.ticker_pattern.findall(text)
        for match in ticker_matches:
            if match in stock_tickers:
                found_tickers.add(match)
                
        company_matches = self.company_pattern.findall(text)
        for match in company_matches:
            ticker = self.name_to_ticker.get(match.lower())
            if ticker:
                found_tickers.add(ticker)
                
        return sorted(list(found_tickers))
        