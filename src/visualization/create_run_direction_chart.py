import plotly.graph_objects as go

def create_run_direction_chart(dates, closing_prices, returns, runs, symbol):
    """
    Create a Plotly chart showing price movements colored by run direction.
    
    Args:
        dates: List of date strings
        closing_prices: List of closing prices
        returns: Pandas Series or list of daily returns
        symbol: Stock symbol string
        
    Returns:
        HTML string of the Plotly chart
    """
    fig = go.Figure()
    
    # Build color and streak info arrays
    colors = []
    streak_info = []
    
    for direction, streak in runs:
        color = "green" if direction == "up" else "red" if direction == "down" else "blue"
        
        for i in range(streak):
            colors.append(color)
            streak_info.append({
                'direction': direction,
                'streak': streak,
                'position_in_streak': i + 1
            })
    
    # Determine maximum segments to plot
    max_segments = min(len(returns), len(colors), len(dates) - 1, len(closing_prices) - 1)
    
    # Plot segments grouped by run
    i = 0
    while i < max_segments:
        current_color = colors[i]
        current_streak_data = streak_info[i]
        
        start_idx = i
        # Group consecutive points in the same run
        while (i < max_segments and 
               colors[i] == current_color and 
               streak_info[i]['direction'] == current_streak_data['direction'] and
               streak_info[i]['streak'] == current_streak_data['streak']):
            i += 1
        
        end_idx = i
        
        # Extract data for this segment
        x_data = dates[start_idx:end_idx + 1]
        y_data = closing_prices[start_idx:end_idx + 1]
        
        direction = current_streak_data['direction'].title()
        streak = current_streak_data['streak']
        
        # Build hover text
        hover_text = []
        for j in range(len(x_data)):
            if j < len(x_data) - 1:
                actual_idx = start_idx + j
                hover_text.append(
                    f"Date: {x_data[j]}<br>"
                    f"Price: ${y_data[j]:.2f}<br>"
                    f"Direction: {direction}<br>"
                    f"Streak Length: {streak} days<br>"
                    f"Day {actual_idx - start_idx + 1} of {streak}"
                )
            else:
                hover_text.append(
                    f"Date: {x_data[j]}<br>"
                    f"Price: ${y_data[j]:.2f}"
                )
        
        # Add trace for this run segment
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode="lines+markers",
            line=dict(color=current_color, width=3),
            marker=dict(size=4, color=current_color),
            name=f"{direction} Run (Length: {streak})",
            text=hover_text,
            hovertemplate="%{text}<extra></extra>",
            showlegend=False
        ))
    
    fig.update_layout(
        title=f'Closing Price over time with Run Directions for {symbol}',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        hovermode='closest',
        height=600
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False)