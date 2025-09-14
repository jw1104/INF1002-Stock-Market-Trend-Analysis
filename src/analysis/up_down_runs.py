import yfinance as yf
import pandas as pd
import numpy as np
from utils.clean_data import clean_data

def calculate_price_changes(prices):
    price_changes = []
    
    for i in range(1, len(prices)):
        price_change = prices[i] - prices[i-1]
        price_changes.append(price_change)
    return price_changes


def calculate_directions(price_changes):
    directions = []
    
    for change in price_changes:
        if change > 0:
            directions.append('up')
        elif change < 0:
            directions.append('down')
        else:
            directions.append('flat')

    return directions
    

def calculate_runs(directions):
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

def analyze_price_runs(data):
    """
    Analyzes given data to obtain run statistics in 3 different directions (up, down, flat)
    
    Parameters:
    data (pd.Series): Closing prices of a stock
    
    Return:
    dictionary containing run statistics
    
    """
    
    prices = clean_data(data)
    price_changes = calculate_price_changes(prices)
    directions = calculate_directions(price_changes)
    runs = calculate_runs(directions)
    
    # create dictionary with run statistics
    results = {
        'total_trading_days': len(prices),
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
        ticker = yf.Ticker('AAPL')
        data = ticker.history('1y')
        results = analyze_price_runs(data['Close'])
        print_run_summary(results)
        
    except ValueError as e:
        print(f'An error occurred: {e}')