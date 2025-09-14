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
    
    cleaned_data = data.dropna().tolist()
    if data.empty:
        raise ValueError("No data for analysis")
    
    if len(cleaned_data) < 2:
        raise ValueError("Insufficient data for analysis")
    
    return cleaned_data