import yfinance as yf

def data_fetcher(ticker, period):
    ticker = ticker.upper()
    period = period.lower()
    stock_data = yf.Ticker(ticker).history(period)
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
