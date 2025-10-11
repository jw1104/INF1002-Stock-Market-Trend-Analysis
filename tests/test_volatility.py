import pytest
from INF1002_Stock_Market_Trend_Analysis.src.analysis.volatility import analyze_volatility, categorize_volatility

class TestVolatilityAnalysis:
    def test_empty_returns_list(self):
        result = analyze_volatility([])
        assert result is None
    
    def test_all_none_values(self):
        result = analyze_volatility([None, None, None])
        assert result is None
    
    def test_mixed_none_and_valid_returns(self):
        returns = [None, 2.0, 3.0, -1.0, None, 1.0]
        result = analyze_volatility(returns)
        
        assert result is not None
        assert result['avg_daily_return'] == 1.25
    
    def test_max_gain_and_loss_identification(self):
        returns = [1.5, -3.2, 5.7, -1.0, 2.3]
        result = analyze_volatility(returns)
        
        assert result['max_gain'] == 5.7
        assert result['max_loss'] == -3.2
    
    def test_negative_average_return(self):
        returns = [-1.0, -2.0, -1.5, -0.5]
        result = analyze_volatility(returns)
        
        assert result['avg_daily_return'] < 0
        assert result['max_loss'] == -2.0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])