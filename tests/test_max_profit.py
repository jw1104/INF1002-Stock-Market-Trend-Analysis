import pytest
import pandas as pd
import datetime as dt
from INF1002_Stock_Market_Trend_Analysis.src.analysis.max_profit import max_profit


class TestMaxProfit:
    """Test suite for max_profit function"""
    
    def test_basic_profit_calculation(self):
        # test basic profit calculation
        dates = pd.date_range(start='2024-01-01', periods=5, freq='D')
        data = pd.DataFrame({
            'Close': [100.0, 110.0, 105.0, 120.0, 115.0]
        }, index=dates)
        
        result = max_profit(data)
        
        assert result['max_profit'] == 20.0
        assert result['buy_date'] == '2024-01-01'
        assert result['buy_price'] == 100.0
        assert result['sell_date'] == '2024-01-04'
        assert result['sell_price'] == 120.0
    
    def test_declining_prices_raises_error(self):
        # test that declining prices raise ValueError
        dates = pd.date_range(start='2024-01-01', periods=5, freq='D')
        data = pd.DataFrame({
            'Close': [100.0, 90.0, 80.0, 70.0, 60.0]
        }, index=dates)
        
        with pytest.raises(ValueError, match="No profit opportunity"):
            max_profit(data)
    
    def test_constant_prices_raises_error(self):
        # test that constant prices raise ValueError
        dates = pd.date_range(start='2024-01-01', periods=5, freq='D')
        data = pd.DataFrame({
            'Close': [100.0, 100.0, 100.0, 100.0, 100.0]
        }, index=dates)
        
        with pytest.raises(ValueError, match="No profit opportunity"):
            max_profit(data)
    
    def test_single_price_point(self):
        # Test with only one price point
        dates = pd.date_range(start='2024-01-01', periods=1, freq='D')
        data = pd.DataFrame({
            'Close': [100.0]
        }, index=dates)
        
        with pytest.raises(ValueError, match="No profit opportunity"):
            max_profit(data)
    
    def test_two_price_points_no_profit(self):
        # test with two price points where no profit is possible
        dates = pd.date_range(start='2024-01-01', periods=2, freq='D')
        data = pd.DataFrame({
            'Close': [120.0, 100.0]
        }, index=dates)
        
        with pytest.raises(ValueError, match="No profit opportunity"):
            max_profit(data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])