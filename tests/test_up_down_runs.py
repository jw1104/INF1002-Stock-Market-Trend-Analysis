import pytest
import pandas as pd
import numpy as np
from INF1002_Stock_Market_Trend_Analysis.src.analysis.up_down_runs import calculate_directions, calculate_runs, analyze_runs

class TestCalculateDirections:
    """
    tests for calculate_directions function
    """
    
    def test_mixed_price_changes(self):
        # test case for positive, negative and zero values
        price_changes = [1.5, -2.0, 0, 3.2, -1.1]
        result = calculate_directions(price_changes)
        expected = ['up', 'down', 'flat', 'up', 'down']
        assert result == expected
    
    def test_pandas_series_with_nan(self):
        # test case for input with missing values
        price_changes = [1.5, np.nan, -2.0, 0, np.nan, 2.5]
        result = calculate_directions(price_changes)
        expected = ['up', 'down', 'flat', 'up']
        assert result == expected
    
    def test_edge_values(self):
        # test case for zero and small values
        price_changes = [0.0001, -0.0001, 0, 1e-10, -1e-10]
        result = calculate_directions(price_changes)
        expected = ['up', 'down', 'flat', 'up', 'down']
        assert result == expected
    
    def test_empty_and_single_value(self):
        # test case for zero or only one value
        with pytest.raises(ValueError):
            calculate_directions([])
            
        assert calculate_directions([2.5]) == ['up']
        assert calculate_directions([-1.0]) == ['down']


class TestCalculateRuns:
    """
    tests for calculate_runs function
    """
    
    def test_multiple_runs_mixed_directions(self):
        # test for mulitple consecutive runs of different directions
        directions = ['up', 'up', 'down', 'down', 'down', 'flat', 'up']
        result = calculate_runs(directions)
        expected = [('up', 2), ('down', 3), ('flat', 1), ('up', 1)]
        assert result == expected
    
    def test_alternating_directions(self):
        # test for alternating directions with no consecutive runs
        directions = ['up', 'down', 'up', 'flat', 'down']
        result = calculate_runs(directions)
        expected = [('up', 1), ('down', 1), ('up', 1), ('flat', 1), ('down', 1)]
        assert result == expected
    
    def test_single_long_run(self):
        # test for a single direction
        directions = ['up', 'up', 'up', 'up', 'up']
        result = calculate_runs(directions)
        expected = [('up', 5)]
        assert result == expected
        
    def test_empty_and_single_input(self):
        # test for empty or single run input
        with pytest.raises(ValueError):
            calculate_runs([])
            
        assert calculate_runs(['up']) == [('up', 1)]
        
        
class TestAnalyzeRuns:
    """Test suite for analyze_runs function"""
    
    def test_mixed_runs_calculation(self):
        # test case for mixed upward and downward runs
        runs = [
            ('up', 3),
            ('down', 2),
            ('up', 5),
            ('down', 4),
            ('up', 2)
        ]
        result = analyze_runs(runs)
        
        assert result["avg_upward_run"] == 3.3
        assert result["avg_downward_run"] == 3.0
        assert result["max_upward_run"] == 5
        assert result["max_downward_run"] == 4
        assert result["current_run"] == 2
        assert result["current_run_type"] == 'up'
    
    def test_only_upward_runs(self):
        # test when all runs are one direction
        runs = [
            ('up', 4),
            ('up', 6),
            ('up', 2)
        ]
        result = analyze_runs(runs)
        
        assert result["avg_upward_run"] == 4.0
        assert result["avg_downward_run"] == 0
        assert result["max_upward_run"] == 6
        assert result["max_downward_run"] == 0
        assert result["current_run"] == 2
        assert result["current_run_type"] == 'up'
    
    def test_single_run(self):
        # test with only one run
        runs = [('up', 5)]
        result = analyze_runs(runs)
        
        assert result["avg_upward_run"] == 5.0
        assert result["avg_downward_run"] == 0
        assert result["max_upward_run"] == 5
        assert result["max_downward_run"] == 0
        assert result["current_run"] == 5
        assert result["current_run_type"] == 'up'
    
    def test_empty_runs_raises_error(self):
        #Test that empty runs list raises ValueError
        with pytest.raises(ValueError, match="No run data provided"):
            analyze_runs([])

        
if __name__ == '__main__':
    pytest.main([__file__, '-v'])