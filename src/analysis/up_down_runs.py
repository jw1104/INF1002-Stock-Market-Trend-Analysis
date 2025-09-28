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
    

def calculate_run_stats(runs, target_direction):
    filtered_run = [length for direction, length in runs if direction == target_direction]
    
    return {
        'total_days': sum(filtered_run) if filtered_run else 0,
        'total_runs': len(filtered_run),
        'longest_streak': max(filtered_run) if filtered_run else 0,
        'runs': filtered_run
    }
    
 
def analyze_runs(data):
    price_changes = daily_returns(data)
    directions = calculate_directions(price_changes)
    runs = calculate_runs(directions)
    
    return runs
   

def analysis_summary(runs):
    """
    Analyzes given data to obtain run statistics in 3 different directions (up, down, flat)
    
    Parameters:
    data (pd.Series): Closing prices of a stock
    
    Return:
    dictionary containing run statistics
    
    """
    total_trading_days = 0
    
    # calculate number of trading days
    for run in runs:
        total_trading_days += run[1]
        
    # create dictionary with run statistics
    results = {
        'total_trading_days': total_trading_days,
        'upward_runs': calculate_run_stats(runs, 'up'),
        'downward_runs': calculate_run_stats(runs, 'down'),
        'flat_runs': calculate_run_stats(runs, 'flat')
    }
    
    return results




def print_run_summary(results):
    """
    Print a formatted summary of the run analysis.
    """
    if 'error' in results:
        print(f"Error: {results['error']}")
        return
    
    print(f"Number of trading days: {results['total_trading_days']}")
    
    print(f"\n--- UPWARD RUNS ---")
    print(f"Number of upward runs: {results['upward_runs']['total_runs']}")
    print(f"Total upward days: {results['upward_runs']['total_days']}")
    print(f"Longest upward streak: {results['upward_runs']['longest_streak']} days")
    
    print(f"\n--- DOWNWARD RUNS ---")
    print(f"Number of downward runs: {results['downward_runs']['total_runs']}")
    print(f"Total downward days: {results['downward_runs']['total_days']}")
    print(f"Longest downward streak: {results['downward_runs']['longest_streak']} days")
    
    print(f"\n--- FLAT RUNS ---")
    print(f"Number of flat runs: {results['flat_runs']['total_runs']}")
    print(f"Number of flat days: {results['flat_runs']['total_days']}")
    print(f"Longest flat streak: {results['flat_runs']['longest_streak']} days")


if __name__ == "__main__":
    try: 
        data = data_fetcher("AAPL", "3y")
        runs = analyze_runs(data)
        results = analysis_summary(runs)
        print_run_summary(results)
        
    except ValueError as e:
        print(f'An error occurred: {e}')