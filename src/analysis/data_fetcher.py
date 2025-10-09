import yfinance as yf

def data_fetcher(ticker, period=None, start_date=None, end_date=None):
    """
    Fetches historical stock data using yfinance and cleans it, takes
    either time period or start and end dates
    
    Args:
        ticker: Stock ticker symbol (str)
        period: Data period (e.g., '1y', '3mo') (str)
        start_date: Start date for data (str, 'YYYY-MM-DD')
        end_date: End date for data (str, 'YYYY-MM-DD')
        
    Returns:
        pd.DataFrame: Cleaned historical stock data
    """
    
    ticker = ticker.upper()
    
    if start_date and end_date:
        stock_data = yf.Ticker(ticker).history(start=start_date, end=end_date)
    elif period:
        period = period.lower()
        stock_data = yf.Ticker(ticker).history(period=period)
    else:
        raise ValueError("Either period or both start_date and end_date must be provided")
    
    cleaned_data = clean_data(stock_data)
    
    return cleaned_data


def clean_data(data):
    """
    Removes all NaN values and ensures at least 2 values for analysis
    
    Args:
        data: pd.Series
        
    Returns:
        List of clean data
        
    Raises:
        ValueError: If insufficient data after cleaning
    """
    
    if data is None or data.empty:
        raise ValueError("No data for analysis")
   
    # Check if 'Close' column exists
    if 'Close' not in data.columns:
        raise ValueError("No Closing price data")
   
    # Remove rows where there is NaN
    cleaned_data = data.dropna()
   
    # Check if we have enough data after cleaning
    if len(cleaned_data) < 2:
        raise ValueError("Insufficient data for analysis (less than 2 data points)")
   
    return cleaned_data