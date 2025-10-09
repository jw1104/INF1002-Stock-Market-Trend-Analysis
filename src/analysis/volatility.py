def analyze_volatility(returns):
    """
    Analyze volatility from your daily returns function
    
    Args:
        returns: List of daily returns (with None for first day)
        
    Returns:
        dict: Key volatility statistics
    """
    
    # Remove None values
    clean_returns = [r for r in returns if r is not None]
    
    if not clean_returns:
        return None
    
    # Calculate average return
    avg_return = sum(clean_returns) / len(clean_returns)
    
    # Calculate standard deviation (volatility)
    squared_diffs = [(r - avg_return) ** 2 for r in clean_returns]
    variance = sum(squared_diffs) / len(squared_diffs)
    daily_vol = variance ** 0.5
    
    # Annualized volatility (daily vol * sqrt(252 trading days))
    annual_vol = daily_vol * (252 ** 0.5)
    
    return {
        'daily_volatility': round(daily_vol, 2),
        'annualized_volatility': round(annual_vol, 1),
        'avg_daily_return': round(avg_return, 2),
        'max_gain': round(max(clean_returns), 2),
        'max_loss': round(min(clean_returns), 2),
        'volatility_level': categorize_volatility(annual_vol)
    }

def categorize_volatility(annual_vol):
    """
    Categorize volatility level based on annualized volatility
    
    Args:
        annual_vol: Annualized volatility percentage
    
    Returns:
        str: Volatility category
    """
    
    if annual_vol < 20:
        return "Low Volatility - Stable Stock"
    elif annual_vol < 35:
        return "Moderate Volatility - Normal Risk"
    else:
        return "High Volatility - Risky Stock"