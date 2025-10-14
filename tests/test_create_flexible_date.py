import pytest
from test_utils import FlexibleDateTestRunner

# Initialize the test runner (will handle environment setup automatically)
test_runner = FlexibleDateTestRunner()


class TestCreateFlexibleDate:
    """Test FlexibleDate creation from string inputs in both Python and TypeScript."""
    
    def test_simple_date_creation(self):
        """Test basic date string parsing with both implementations."""
        test_data = {
            "input": "2023-05-15",
            "expected": {
                "likelyYear": 2023,
                "likelyMonth": 5,
                "likelyDay": 15
            },
            "mocks": {}  # No mocking needed for this simple test
        }
        
        # Run the test against both implementations
        py_result, ts_result = test_runner.run_dual_test(
            "create_flexible_date",
            "createFlexibleDate", 
            test_data
        )
        
        # Assert both implementations return expected results
        assert py_result == test_data["expected"], f"Python result {py_result} != expected {test_data['expected']}"
        assert ts_result == test_data["expected"], f"TypeScript result {ts_result} != expected {test_data['expected']}"
        
        # Assert both implementations return identical results (parity check)
        assert py_result == ts_result, f"Implementation mismatch: Python={py_result}, TypeScript={ts_result}"
        
        print(f"SUCCESS: Both implementations correctly parsed '{test_data['input']}' as {py_result}")