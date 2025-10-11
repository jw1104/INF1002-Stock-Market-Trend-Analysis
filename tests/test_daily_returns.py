import pytest
import pandas as pd
import numpy as np
from INF1002_Stock_Market_Trend_Analysis.src.analysis.daily_returns import daily_returns

class TestDailyReturns:
    """tests for daily_returns function"""
    
    def test_basic_calculation(self):
        # test case for basic percentage return calculation with positive and negative returns
        prices = [100, 110, 105, 100]
        result = daily_returns(prices)
        
        assert result[0] is None  # First value should always be None
        assert result[1] == 10.0  # (110-100)/100 * 100 = 10%
        assert result[2] == -4.55  # (105-110)/110 * 100 = -4.545...
        assert result[3] == -4.76  # (100-105)/105 * 100 = -4.762...
    
    def test_nan_values(self):
        # test handling of NaN values in the series
        prices = pd.Series([100, np.nan, 110, 120])
        result = daily_returns(prices)
        
        assert result[0] is None
        assert result[1] is None  # NaN should result in None
        assert result[2] is None  # Previous value is NaN, so result is None
        assert result[3] == 9.09  # (120-110)/110 * 100
    
    def test_zero_previous_close(self):
        # test case for division by zero handling when previous close is zero
        prices = pd.Series([100, 0, 50])
        result = daily_returns(prices)
        
        assert result[0] is None
        assert result[1] == -100.0  # (0-100)/100 * 100 = -100%
        assert result[2] is None  # Division by zero should return None
    
    def test_empty_and_single_price(self):
        # test edge cases: empty series and single price
        empty_result = daily_returns(pd.Series([]))
        assert empty_result == []
        
        single_result = daily_returns(pd.Series([100]))
        assert len(single_result) == 1
        assert single_result[0] is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])