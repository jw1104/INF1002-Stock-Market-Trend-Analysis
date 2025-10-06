import yfinance as yf
import pandas as pd


def calculate_directions(price_changes):
    """
    Convert a list of price changes into directional indicators: 'up', 'down', 'flat'.
    
    Args:
        price_changes: List of daily percentage changes (can include None for missing data)
        
    Returns:
        List of directions corresponding to price changes
    """
    
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
            run_streak += 1 # Increment current run streak
        else:
            runs.append((current_direction, run_streak)) # End of current run streak
            current_direction = directions[i] # Change in direction
            run_streak = 1 # Reset current run streak
    
    runs.append((current_direction, run_streak)) # Append the last run
    
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
    
    # Separate runs by direction
    upward_runs = [streak for direction, streak in runs if direction == 'up']
    downward_runs = [streak for direction, streak in runs if direction == 'down']
    flat_runs = [streak for direction, streak in runs if direction == 'flat']
    
    # Obtain average run lengths per direction
    avg_upward = sum(upward_runs) / len(upward_runs) if upward_runs else 0
    avg_downward = sum(downward_runs) / len(downward_runs) if downward_runs else 0
    avg_flat = sum(flat_runs) / len(flat_runs) if flat_runs else 0
    
    current_direction, current_streak = runs[-1]
    
    return {
        "avg_upward_run": round(avg_upward, 1),
        "avg_downward_run":round(avg_downward, 1),
        "max_upward_run": max(upward_runs) if upward_runs else 0,
        "max_downward_run": max(downward_runs) if downward_runs else 0,
        "current_run": current_streak,
        "current_run_type": current_direction
    }