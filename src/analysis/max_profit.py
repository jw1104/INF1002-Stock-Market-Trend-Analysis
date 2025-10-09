import yfinance as yf
import datetime as dt

def max_profit(data):
    """
    Trading Algorithm - Max Profit Calculator
    
    Finds the maximum profit from a single buy-sell transaction.
    Uses Kadane's algorithm variant with O(n) time complexity.
    
    Time Complexity: O(n) where n is the number of data points
    Space Complexity: O(1) - only stores scalar variables
    
    Args:
        data: DataFrame with 'Close' prices and datetime index
        
    Returns:
        dict: Contains max_profit, buy_date, buy_price, sell_date, sell_price
        
    Raises:
        ValueError: If no profit opportunity exists
    """
    # Extract closing prices from the DataFrame
    close_prices = data['Close']
    
    # Initialize tracking variables
    min_price = float('inf')  # Set to infinity initially to check for min
    max_profit = 0.0  # Track the best profit opportunity found
    buy_time = sell_time = None  # Initialize buy and sell times
    min_index = None # Track index of minimum price
    
    # O(n) - Single pass through all prices
    for i, price in enumerate(close_prices):
        # Update minimum price and its index if we find a new low
        if price < min_price:
            min_price = price
            min_index = i
        
        # Calculate potential profit if we bought at min_price and sold at current price
        profit = price - min_price
        
        # Update our best trade if this profit exceeds previous maximum
        if profit > max_profit:
            max_profit = profit
            buy_time = min_index  # Buy at the minimum price point
            sell_time = i  # Sell at current price point
    
    # Validate that a profitable trade opportunity exists
    if max_profit > 0 and buy_time is not None and sell_time is not None:
        # Extract and format buy transaction details
        buy_date = data.index[buy_time].strftime("%Y-%m-%d")
        buy_price = data["Close"].iloc[buy_time]
        
        # Extract and format sell transaction details
        sell_date = data.index[sell_time].strftime("%Y-%m-%d")
        sell_price = data["Close"].iloc[sell_time]
        
        # Return formatted results with all values rounded to 2 decimal places
        return {
            "max_profit": round(max_profit, 2),
            "buy_date": buy_date,
            "buy_price": buy_price.round(2),
            "sell_date": sell_date,
            "sell_price": sell_price.round(2)
        }
    else:
        # Raise error if no profitable trade was found (e.g., prices only declined)
        raise ValueError(f"No profit opportunity.")
    