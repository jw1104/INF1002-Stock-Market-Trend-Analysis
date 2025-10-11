import pytest
import pandas as pd
import numpy as np
from INF1002_Stock_Market_Trend_Analysis.src.analysis.up_down_runs import calculate_directions, calculate_runs, analyze_runs

class TestCalculateDirections:
    def test_mixed_price_changes(self):
        price_changes = [1.5, -2.0, 0, 3.2, -1.1]
        result = calculate_directions(price_changes)
        expected = ['up', 'down', 'flat', 'up', 'down']
        assert result == expected
    
    def test_pandas_series_with_nan(self):
        price_changes = [1.5, np.nan, -2.0, 0, np.nan, 2.5]
        result = calculate_directions(price_changes)
        expected = ['up', 'down', 'flat', 'up']
        assert result == expected
    
    def test_edge_values(self):
        price_changes = [0.0001, -0.0001, 0, 1e-10, -1e-10]
        result = calculate_directions(price_changes)
        expected = ['up', 'down', 'flat', 'up', 'down']
        assert result == expected
    
    def test_empty_and_single_value(self):
        with pytest.raises(ValueError):
            calculate_directions([])
            
        assert calculate_directions([2.5]) == ['up']
        assert calculate_directions([-1.0]) == ['down']


class TestCalculateRuns:
    def test_multiple_runs_mixed_directions(self):
        directions = ['up', 'up', 'down', 'down', 'down', 'flat', 'up']
        result = calculate_runs(directions)
        expected = [('up', 2), ('down', 3), ('flat', 1), ('up', 1)]
        assert result == expected
    
    def test_alternating_directions(self):
        directions = ['up', 'down', 'up', 'flat', 'down']
        result = calculate_runs(directions)
        expected = [('up', 1), ('down', 1), ('up', 1), ('flat', 1), ('down', 1)]
        assert result == expected
    
    def test_single_long_run(self):
        directions = ['up', 'up', 'up', 'up', 'up']
        result = calculate_runs(directions)
        expected = [('up', 5)]
        assert result == expected
        
    def test_empty_and_single_input(self):
        with pytest.raises(ValueError):
            calculate_runs([])
            
        assert calculate_runs(['up']) == [('up', 1)]
        
        
class TestAnalyzeRuns:
    def test_mixed_runs_calculation(self):
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
        runs = [('up', 5)]
        result = analyze_runs(runs)
        
        assert result["avg_upward_run"] == 5.0
        assert result["avg_downward_run"] == 0
        assert result["max_upward_run"] == 5
        assert result["max_downward_run"] == 0
        assert result["current_run"] == 5
        assert result["current_run_type"] == 'up'
    
    def test_empty_runs_raises_error(self):
        with pytest.raises(ValueError, match="No run data provided"):
            analyze_runs([])

        
if __name__ == '__main__':
    pytest.main([__file__, '-v'])