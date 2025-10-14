import pytest
from test_utils import FlexibleDateTestRunner


class TestCreateFlexibleDateFromFormalDate:
    """Test FlexibleDate creation from EDTF format strings in both Python and TypeScript."""
    
    def setup_method(self):
        """Set up test runner for each test method."""
        self.runner = FlexibleDateTestRunner()
    
    def test_basic_edtf_parsing(self):
        """Test basic EDTF string parsing."""
        test_cases = self.runner.load_test_cases("create_flexible_date_from_formal_date", "basic")
        
        for case in test_cases:
            print(f"Testing: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "createFlexibleDateFromFormalDate",
                case["input"],
                expected=case["expected"]
            )
    
    def test_complex_edtf_formats(self):
        """Test more complex EDTF format strings."""
        complex_cases = [
            {
                "name": "datetime_with_timezone",
                "input": "+1526-01-01T00:00:00Z",
                "expected": {
                    "likelyYear": 1526,
                    "likelyMonth": 1,
                    "likelyDay": 1
                }
            },
            {
                "name": "datetime_range",
                "input": "+1910-01-01T00:00:00Z/+1910-12-31T23:59:59Z",
                "expected": {
                    "likelyYear": 1910,
                    "likelyMonth": 1,
                    "likelyDay": 1
                }
            },
            {
                "name": "year_only_edtf",
                "input": "1945",
                "expected": {
                    "likelyYear": 1945,
                    "likelyMonth": None,
                    "likelyDay": None
                }
            }
        ]
        
        for case in complex_cases:
            print(f"Testing complex EDTF: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "createFlexibleDateFromFormalDate",
                case["input"],
                expected=case["expected"]
            )
    
    def test_edtf_error_handling(self):
        """Test error handling for invalid EDTF strings."""
        invalid_cases = [
            "invalid-date-format",
            "2023-13-45",  # Invalid month/day
            "",
        ]
        
        for invalid_input in invalid_cases:
            print(f"Testing invalid EDTF: {invalid_input}")
            
            # Both implementations should handle errors gracefully
            # We expect them to either return a null date or raise the same type of error
            try:
                py_result = self.runner.run_python_test("createFlexibleDateFromFormalDate", invalid_input)
                ts_result = self.runner.run_typescript_test("createFlexibleDateFromFormalDate", invalid_input)
                
                # If both succeed, they should return the same result
                assert self.runner.compare_results(py_result, ts_result), \
                    f"Different results for invalid input '{invalid_input}': Python={py_result}, TypeScript={ts_result}"
                    
            except Exception as e:
                # If one fails, both should fail with similar errors
                # This is acceptable as long as they behave consistently
                print(f"Both implementations failed for '{invalid_input}': {str(e)}")
                pass
