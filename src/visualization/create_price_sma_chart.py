import plotly.graph_objs as go


def create_price_sma_chart(dates, closing_prices, sma_data, symbol):
    """
    Create a Plotly chart showing closing prices and multiple SMAs with crossover markers.
    
    Args:
        dates: List of date strings
        closing_prices: List of closing prices
        sma_data: Dictionary with 'short', 'medium', 'long' keys, each containing 'values' and 'period'
        symbol: Stock symbol string
        
    Returns:
        HTML string of the Plotly chart
    """
    fig = go.Figure()
    
    # Add closing price trace
    fig.add_trace(go.Scatter(
        x=dates,
        y=closing_prices,
        mode='lines',
        name='Closing Price',
        line=dict(color='#1f77b4', width=2),
        hovertemplate='Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'
    ))
    
    # Add SMA traces with different colors
    sma_colors = {
        'short': '#2ca02c',   # Green
        'medium': '#ff7f0e',  # Orange
        'long': '#d62728'     # Red
    }
    
    sma_names = {
        'short': 'Short',
        'medium': 'Medium',
        'long': 'Long'
    }
    
    for key in ['short', 'medium', 'long']:
        period = sma_data[key]['period']
        values = sma_data[key]['values']
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines',
            name=f'{sma_names[key]} SMA ({period})',
            line=dict(color=sma_colors[key], width=2, dash='dash'),
            hovertemplate=f'Date: %{{x}}<br>SMA-{period}: $%{{y:.2f}}<extra></extra>'
        ))
    
    # Detect crossovers and add markers
    crossovers = detect_crossovers(
        dates,
        sma_data['short']['values'],
        sma_data['medium']['values'],
        sma_data['long']['values']
    )
    
    # Add crossover markers
    for crossover in crossovers:
        fig.add_trace(go.Scatter(
            x=[crossover['date']],
            y=[crossover['price']],
            mode='markers+text',
            name=crossover['type'],
            marker=dict(
                size=15,
                color=crossover['color'],
                symbol='star',
                line=dict(color='white', width=2)
            ),
            text=[crossover['label']],
            textposition='top center',
            textfont=dict(size=10, color=crossover['color']),
            hovertemplate=f"{crossover['type']}<br>Date: {crossover['date']}<br>Price: ${crossover['price']:.2f}<extra></extra>",
            showlegend=False
        ))
    
    fig.update_layout(
        title=f'Closing Prices vs Multiple SMAs for {symbol}',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        hovermode='x unified',
        width=1000,
        height=600,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False)


def detect_crossovers(dates, sma_short, sma_medium, sma_long):
    """
    Detect crossover points between SMA lines.
    
    Args:
        dates: List of date strings
        sma_short: List of short SMA values
        sma_medium: List of medium SMA values
        sma_long: List of long SMA values
        
    Returns:
        List of crossover dictionaries with date, price, type, color, and label
    """
    crossovers = []
    
    # Check for Golden Cross and Death Cross (medium crosses long)
    for i in range(1, len(dates)):
        # Skip if any value is None
        if (sma_medium[i] is None or sma_medium[i-1] is None or 
            sma_long[i] is None or sma_long[i-1] is None):
            continue
        
        # Golden Cross: medium crosses above long
        if sma_medium[i-1] <= sma_long[i-1] and sma_medium[i] > sma_long[i]:
            crossovers.append({
                'date': dates[i],
                'price': sma_medium[i],
                'type': 'Golden Cross',
                'color': 'gold',
                'label': '★ GC'
            })
        
        # Death Cross: medium crosses below long
        elif sma_medium[i-1] >= sma_long[i-1] and sma_medium[i] < sma_long[i]:
            crossovers.append({
                'date': dates[i],
                'price': sma_medium[i],
                'type': 'Death Cross',
                'color': 'darkred',
                'label': '✕ DC'
            })
    
    # Check for short-medium crossovers
    for i in range(1, len(dates)):
        if (sma_short[i] is None or sma_short[i-1] is None or 
            sma_medium[i] is None or sma_medium[i-1] is None):
            continue
        
        # Short crosses above medium (bullish)
        if sma_short[i-1] <= sma_medium[i-1] and sma_short[i] > sma_medium[i]:
            crossovers.append({
                'date': dates[i],
                'price': sma_short[i],
                'type': 'Bullish Cross',
                'color': 'limegreen',
                'label': '↑'
            })
        
        # Short crosses below medium (bearish)
        elif sma_short[i-1] >= sma_medium[i-1] and sma_short[i] < sma_medium[i]:
            crossovers.append({
                'date': dates[i],
                'price': sma_short[i],
                'type': 'Bearish Cross',
                'color': 'orangered',
                'label': '↓'
            })
    
    return crossovers