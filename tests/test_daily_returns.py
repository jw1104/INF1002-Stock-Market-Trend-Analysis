import pytest
import pandas as pd
import numpy as np
from INF1002_Stock_Market_Trend_Analysis.src.analysis.daily_returns import daily_returns

class TestDailyReturns: 
    def test_basic_calculation(self):
        prices = [100, 110, 105, 100]
        result = daily_returns(prices)
        
        assert result[0] is None
        assert result[1] == 10.0
        assert result[2] == -4.55
        assert result[3] == -4.76
    
    def test_nan_values(self):
        prices = pd.Series([100, np.nan, 110, 120])
        result = daily_returns(prices)
        
        assert result[0] is None
        assert result[1] is None
        assert result[2] is None
        assert result[3] == 9.09
    
    def test_zero_previous_close(self):
        prices = pd.Series([100, 0, 50])
        result = daily_returns(prices)
        
        assert result[0] is None
        assert result[1] == -100.0
        assert result[2] is None
    
    def test_empty_and_single_price(self):
        empty_result = daily_returns(pd.Series([]))
        assert empty_result == []
        
        single_result = daily_returns(pd.Series([100]))
        assert len(single_result) == 1
        assert single_result[0] is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])