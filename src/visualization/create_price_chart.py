import plotly.graph_objects as go

def create_price_chart(dates, closing_prices, returns, runs, symbol, max_profit):
    """
    Create a Plotly chart showing price movements colored by run direction and maximum profit.
    
    Args:
        dates: List of date strings
        closing_prices: List of closing prices
        returns: Pandas Series or list of daily returns
        runs: List of tuples (direction, streak_length)
        symbol: Stock symbol string
        max_profit: Dict from max_profit function
        
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
   
    # Add max profit visualization if data is provided
    if max_profit:
        buy_date = max_profit['buy_date']
        buy_price = max_profit['buy_price']
        sell_date = max_profit['sell_date']
        sell_price = max_profit['sell_price']
        profit = max_profit['max_profit']
        profit_pct = (profit / buy_price) * 100
       
        # Add buy marker (green circle)
        fig.add_trace(go.Scatter(
            x=[buy_date],
            y=[buy_price],
            mode='markers+text',
            marker=dict(
                size=15,
                color='lime',
                symbol='circle',
                line=dict(color='darkgreen', width=3)
            ),
            name='Optimal Buy',
            text=['BUY'],
            textposition='bottom center',
            textfont=dict(size=10, color='darkgreen', family='Arial Black'),
            hovertemplate=f'<b>BUY</b><br>Date: {buy_date}<br>Price: ${buy_price:.2f}<extra></extra>',
            showlegend=True
        ))
       
        # Add sell marker (red circle)
        fig.add_trace(go.Scatter(
            x=[sell_date],
            y=[sell_price],
            mode='markers+text',
            marker=dict(
                size=15,
                color='orangered',
                symbol='circle',
                line=dict(color='darkred', width=3)
            ),
            name='Optimal Sell',
            text=['SELL'],
            textposition='top center',
            textfont=dict(size=10, color='darkred', family='Arial Black'),
            hovertemplate=f'<b>SELL</b><br>Date: {sell_date}<br>Price: ${sell_price:.2f}<extra></extra>',
            showlegend=True
        ))
       
        # Add connecting line with arrow
        fig.add_trace(go.Scatter(
            x=[buy_date, sell_date],
            y=[buy_price, sell_price],
            mode='lines',
            line=dict(color='gold', width=2, dash='dash'),
            name='Max Profit Trade',
            hovertemplate=f'<b>Max Profit Trade</b><br>Profit: ${profit:.2f} ({profit_pct:.2f}%)<extra></extra>',
            showlegend=True
        ))
       
        # Add annotation showing profit
        mid_x_idx = dates.index(buy_date) + (dates.index(sell_date) - dates.index(buy_date)) // 2
        mid_date = dates[mid_x_idx] if mid_x_idx < len(dates) else sell_date
        mid_price = (buy_price + sell_price) / 2
       
        fig.add_annotation(
            x=mid_date,
            y=mid_price,
            text=f"<b>Max Profit</b><br>${profit:.2f}<br>({profit_pct:.1f}%)",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="gold",
            ax=0,
            ay=-60,
            bgcolor="rgba(255, 215, 0, 0.8)",
            bordercolor="goldenrod",
            borderwidth=2,
            borderpad=6,
            font=dict(size=11, color="black", family="Arial Black")
        )
   
    fig.update_layout(
        title=f'Closing Price over time with Runs and Maximum Profit for {symbol}',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        hovermode='closest',
        height=600,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="gray",
            borderwidth=1
        )
    )
   
    return fig.to_html(full_html=False, include_plotlyjs=False)