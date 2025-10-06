import yfinance as yf
import datetime as dt
from data_fetcher import data_fetcher


def find_optimal_trade(close_prices):
    """
    Find the optimal buy and sell indices for maximum profit.
    
    Uses Kadane's algorithm variant: tracks minimum price seen so far and calculates
    potential profit at each point by selling at current price.
    
    Time Complexity: O(n) where n is the number of data points
    Space Complexity: O(1) - only stores scalar variables
    
    Args:
        close_prices: Series of closing prices
        
    Returns:
        tuple: (max_profit, buy_index, sell_index) or (0, None, None) if no profit
    """
    min_price = float('inf')  # Track the lowest price encountered so far
    max_profit = 0.0  # Track the best profit opportunity found
    buy_index = None  # Index where we should buy
    sell_index = None  # Index where we should sell
    min_index = None  # Index of the current minimum price
    
    # O(n) - iterate through all prices exactly once
    for i, price in enumerate(close_prices):
        # Update minimum price and its index if we find a new low
        if price < min_price:
            min_price = price
            min_index = i
        
        # Calculate profit if we bought at min_price and sold at current price
        profit = price - min_price
        
        # Update our best trade if this profit exceeds previous maximum
        if profit > max_profit:
            max_profit = profit
            buy_index = min_index  # Buy at the minimum price point
            sell_index = i  # Sell at current price point
    
    return max_profit, buy_index, sell_index


def format_trade_result(data, max_profit, buy_index, sell_index):
    """
    Format trade results into a readable dictionary with dates and prices.
    
    Time Complexity: O(1) - constant time index lookups and formatting
    
    Args:
        data: DataFrame with 'Close' prices and datetime index
        max_profit: Maximum profit amount
        buy_index: Index of buy date in the DataFrame
        sell_index: Index of sell date in the DataFrame
        
    Returns:
        dict: Formatted trade details with dates, prices, and profit
    """
    # Extract dates from DataFrame index and format as YYYY-MM-DD
    buy_date = data.index[buy_index].strftime("%Y-%m-%d")
    sell_date = data.index[sell_index].strftime("%Y-%m-%d")
    
    # Extract actual prices from the Close column
    buy_price = data["Close"].iloc[buy_index]
    sell_price = data["Close"].iloc[sell_index]
    
    # Return formatted results with all values rounded to 2 decimal places
    return {
        "max_profit": round(max_profit, 2),
        "buy_date": buy_date,
        "buy_price": round(buy_price, 2),
        "sell_date": sell_date,
        "sell_price": round(sell_price, 2)
    }


def validate_trade_opportunity(max_profit, buy_index, sell_index):
    """
    Validate if a profitable trade opportunity exists.
    
    A valid trade requires:
    - Positive profit (max_profit > 0)
    - Valid buy index (not None)
    - Valid sell index (not None)
    
    Args:
        max_profit: Maximum profit amount
        buy_index: Index of buy date
        sell_index: Index of sell date
        
    Returns:
        bool: True if valid profitable trade exists
        
    Raises:
        ValueError: If no profit opportunity exists (e.g., prices only declined)
    """
    # Check all conditions for a valid trade
    if max_profit > 0 and buy_index is not None and sell_index is not None:
        return True
    
    # Raise error if no profitable trade was found
    raise ValueError("No profit opportunity.")


def max_profit(data):
    """
    Find the maximum profit from buying and selling a stock once.
    
    This is the main orchestrator function that coordinates the trading algorithm.
    It finds the single best buy-sell pair that maximizes profit, assuming you can
    only make one transaction (one buy, one sell) and must buy before selling.
    
    Time Complexity: O(n) where n is the number of data points
    - Single pass through close_prices: O(n)
    - All operations inside loop are O(1)
    - Index lookups and formatting: O(1)
    
    Space Complexity: O(1)
    - Only stores a constant number of variables regardless of input size
    
    Args:
        data: DataFrame with 'Close' prices and datetime index
        
    Returns:
        dict: Contains max_profit, buy_date, buy_price, sell_date, sell_price
        
    Raises:
        ValueError: If no profit opportunity exists (e.g., stock only declined)
        
    Example:
        >>> result = max_profit(stock_data)
        >>> print(f"Buy on {result['buy_date']} at ${result['buy_price']}")
        >>> print(f"Sell on {result['sell_date']} at ${result['sell_price']}")
        >>> print(f"Profit: ${result['max_profit']}")
    """
    # Extract the closing prices from the DataFrame
    close_prices = data['Close']
    
    # Step 1: Find the optimal buy and sell points
    max_profit_val, buy_index, sell_index = find_optimal_trade(close_prices)
    
    # Step 2: Validate that a profitable trade exists
    validate_trade_opportunity(max_profit_val, buy_index, sell_index)
    
    # Step 3: Format the results into a user-friendly dictionary
    return format_trade_result(data, max_profit_val, buy_index, sell_index)