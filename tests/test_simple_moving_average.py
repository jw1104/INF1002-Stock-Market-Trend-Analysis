import pytest
import pandas as pd
from INF1002_Stock_Market_Trend_Analysis.src.analysis.simple_moving_average import simple_moving_average

class TestSimpleMovingAverage:
    def test_window_size_one(self):
        prices = [15, 25, 35, 45]
        window_size = 1
        result = simple_moving_average(prices, window_size)
        
        assert len(result) == 4
        assert result == [15.0, 25.0, 35.0, 45.0]
    
    def test_window_size_larger_than_data(self):
        prices = [10, 20, 30]
        window_size = 5
        result = simple_moving_average(prices, window_size)
        
        assert result == []
    
    def test_floating_point_prices(self):
        prices = [10.5, 20.7, 30.2, 40.1]
        window_size = 2
        result = simple_moving_average(prices, window_size)
        
        assert len(result) == 3
        assert result[0] == pytest.approx(15.6)
        assert result[1] == pytest.approx(25.45)
        assert result[2] == pytest.approx(35.15)
    
    def test_empty_list(self):
        prices = []
        window_size = 3
        result = simple_moving_average(prices, window_size)
        
        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])