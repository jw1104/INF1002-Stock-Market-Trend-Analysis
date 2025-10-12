import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_volatility_chart(dates, returns, stats):
    """
    Create visualization for volatility analysis.
    
    Args:
        returns: List of daily returns (with None values)
        stats: Dictionary from analyze_volatility()
        
    Returns:
        Plotly figure html string
    """
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Daily Returns Over Time', 'Returns Distribution'),
        column_widths=[0.6, 0.4]
    )
    
    # Left: Returns timeline
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=returns,
            mode='lines',
            line=dict(color='purple', width=1),
            fill='tozeroy',
            fillcolor='rgba(155, 89, 182, 0.2)',
            name='Daily Returns',
            hovertemplate='Return: %{y:.2f}%<br>Date: %{x}<extra></extra>'
        ),
        row=1, col=1
    )
    
    fig.add_hline(y=0, line_dash="solid", line_color="gray", row=1, col=1)
    fig.add_hline(y=stats['avg_daily_return'], line_dash="dash", 
                  line_color="blue",
                  annotation_text=f"Avg: {stats['avg_daily_return']}%",
                  row=1, col=1)
    
    # Right: Distribution histogram
    fig.add_trace(
        go.Histogram(
            x=returns,
            marker_color='orange',
            nbinsx=30,
            name='Distribution',
            showlegend=False,
            hovertemplate=(
                '<b>Return Range:</b> %{x:.1f}%<br>'
                '<b>Frequency:</b> %{y} days<br>'
                '<extra></extra>'
            ),
            histnorm=''  # Show raw counts
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text = f"Volatility Analysis ({stats['volatility_level']})",
        height=600,
        template='plotly_white',
        hovermode='closest'
    )
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="Return (%)", row=1, col=1)
    fig.update_xaxes(title_text="Return (%)", row=1, col=2)
    fig.update_yaxes(title_text="Frequency", row=1, col=2)
    
    return fig.to_html(full_html=False, include_plotlyjs=False)
