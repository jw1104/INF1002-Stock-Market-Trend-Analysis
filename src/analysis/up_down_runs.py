import yfinance as yf
import pandas as pd
import numpy as np
from .data_fetcher import data_fetcher
from .daily_returns import daily_returns


def calculate_directions(price_changes):
    if not price_changes:
        raise ValueError("No data for analysis")
    
    directions = []
    
    for change in price_changes:
        if pd.isna(change):
            continue
        
        if change > 0:
            directions.append('up')
        elif change < 0:
            directions.append('down')
        else:
            directions.append('flat')

    return directions
    

def calculate_runs(directions):
    if not directions:
        raise ValueError("No data for analysis")
    
    runs = []
    run_streak = 1
    current_direction = directions[0]
    
    for i in range(1, len(directions)):
        if directions[i] == current_direction:
            run_streak += 1 # Increment current run streak
        else:
            runs.append((current_direction, run_streak)) # End of current run streak
            current_direction = directions[i] # Change in direction
            run_streak = 1 # Reset current run streak
    
    runs.append((current_direction, run_streak)) # Append the last run
    
    return runs
    