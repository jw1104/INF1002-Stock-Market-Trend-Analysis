import yfinance as yf
import pandas as pd


def calculate_directions(returns):
    """
    Convert a list of daily returns into directional indicators: 'up', 'down', 'flat'
    
    Args:
        returns: List of daily percentage changes (can include None for missing data)
        
    Returns:
        List of directions corresponding to price changes
    """
    
    if not returns:
        raise ValueError("No data for analysis")
    
    directions = []
    
    for r in returns:
        if pd.isna(r):
            continue
        
        if r > 0:
            directions.append('up')
        elif r < 0:
            directions.append('down')
        else:
            directions.append('flat')

    return directions
    

def calculate_runs(directions):
    """
    Calculate runs of consecutive 'up', 'down', or 'flat' directions.
    
    Args:
        directions: List of directions ('up', 'down', 'flat')
    
    Returns:
        List of tuples (direction, streak_length)
    """
    
    if not directions:
        raise ValueError("No data for analysis")
    
    runs = []
    run_streak = 1
    current_direction = directions[0]
    
    for i in range(1, len(directions)):
        if directions[i] == current_direction:
            run_streak += 1
        else:
            runs.append((current_direction, run_streak))
            current_direction = directions[i]
            run_streak = 1
    
    runs.append((current_direction, run_streak))
    
    return runs


def analyze_runs(runs):
    """
    Produce run statistics including average and maximum run lengths.
    
    Args:
        runs: List of tuples (direction, streak_length)
    
    Returns:
        dict: Contains average and maximum run lengths, current run details
    """
    
    if not runs:
        raise ValueError("No run data provided")
    
    upward_runs = [streak for direction, streak in runs if direction == 'up']
    downward_runs = [streak for direction, streak in runs if direction == 'down']
    
    avg_upward = sum(upward_runs) / len(upward_runs) if upward_runs else 0
    avg_downward = sum(downward_runs) / len(downward_runs) if downward_runs else 0
    
    current_direction, current_streak = runs[-1]
    
    return {
        "avg_upward_run": round(avg_upward, 1),
        "avg_downward_run":round(avg_downward, 1),
        "max_upward_run": max(upward_runs) if upward_runs else 0,
        "max_downward_run": max(downward_runs) if downward_runs else 0,
        "current_run": current_streak,
        "current_run_type": current_direction
    }