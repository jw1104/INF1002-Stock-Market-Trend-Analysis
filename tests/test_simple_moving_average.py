import pytest
import pandas as pd
from INF1002_Stock_Market_Trend_Analysis.src.analysis.simple_moving_average import simple_moving_average



class TestSimpleMovingAverage:
    """Test suite for simple_moving_average function"""
    
    def test_window_size_one(self):
        # test with window size of 1
        prices = [15, 25, 35, 45]
        window_size = 1
        result = simple_moving_average(prices, window_size)
        
        assert len(result) == 4
        assert result == [15.0, 25.0, 35.0, 45.0]
    
    def test_window_size_larger_than_data(self):
        # test when window size is larger than data length
        prices = [10, 20, 30]
        window_size = 5
        result = simple_moving_average(prices, window_size)
        
        assert result == []
    
    def test_floating_point_prices(self):
        # test with floating point prices
        prices = [10.5, 20.7, 30.2, 40.1]
        window_size = 2
        result = simple_moving_average(prices, window_size)
        
        assert len(result) == 3
        assert result[0] == pytest.approx(15.6)
        assert result[1] == pytest.approx(25.45)
        assert result[2] == pytest.approx(35.15)
    
    def test_empty_list(self):
        # test with empty price list
        prices = []
        window_size = 3
        result = simple_moving_average(prices, window_size)
        
        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])