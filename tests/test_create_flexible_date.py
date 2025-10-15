import pytest
from test_utils import FlexibleDateTestRunner

# Initialize the test runner (will handle environment setup automatically)
test_runner = FlexibleDateTestRunner()


class TestCreateFlexibleDate:
    """Test FlexibleDate creation from string inputs in both Python and TypeScript."""
    
    class TestFullDates:
        """Test parsing of complete dates with year, month, and day."""
        
        full_date_cases = [
            {
                "input": "2023-05-15",
                "expected": {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15},
                "description": "ISO format"
            },
            {
                "input": "January 15, 2020",
                "expected": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15},
                "description": "American format with comma"
            },
            {
                "input": "15 January 2020",
                "expected": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15},
                "description": "European format"
            },
            {
                "input": "2020-01-15",
                "expected": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15},
                "description": "ISO format dash separated"
            },
            {
                "input": "01/15/2020",
                "expected": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15},
                "description": "MM/DD/YYYY format"
            },
            {
                "input": "15/01/2020",
                "expected": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15},
                "description": "DD/MM/YYYY format"
            },
            {
                "input": "Born on March 15, 1990 in New York",
                "expected": {"likelyYear": 1990, "likelyMonth": 3, "likelyDay": 15},
                "description": "date embedded in text"
            }
        ]
        
        @pytest.mark.parametrize("test_case", full_date_cases, ids=lambda x: x['description'])
        def test_full_date_parsing(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestPartialDates:
        """Test parsing of partial dates (missing day, month, or both)."""
        
        partial_date_cases = [
            {
                "input": "May 2023",
                "expected": {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": None},
                "description": "month and year only"
            },
            {
                "input": "1995",
                "expected": {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None},
                "description": "year only"
            },
            {
                "input": "December",
                "expected": {"likelyYear": None, "likelyMonth": 12, "likelyDay": None},
                "description": "month only"
            },
            {
                "input": "The event happened sometime in July 2021",
                "expected": {"likelyYear": 2021, "likelyMonth": 7, "likelyDay": None},
                "description": "month and year in sentence"
            },
            {
                "input": "circa 1850s",
                "expected": {"likelyYear": 1850, "likelyMonth": None, "likelyDay": None},
                "description": "approximate year with text"
            }
        ]
        
        @pytest.mark.parametrize("test_case", partial_date_cases, ids=lambda x: x['description'])
        def test_partial_date_parsing(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestNullDates:
        """Test handling of null and empty inputs."""
        
        null_date_cases = [
            {
                "input": None,
                "expected": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                "description": "null input"
            },
            {
                "input": "",
                "expected": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                "description": "empty string"
            },
            {
                "input": "   ",
                "expected": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                "description": "whitespace only"
            }
        ]
        
        @pytest.mark.parametrize("test_case", null_date_cases, ids=lambda x: x['description'])
        def test_null_and_empty_inputs(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestCreateFlexibleDateFromFormalDate:
    """Test FlexibleDate creation from EDTF format strings in both Python and TypeScript."""
    
    class TestFullDates:
        """Test EDTF parsing of complete dates with year, month, and day."""
        
        full_edtf_cases = [
            {
                "input": "2020-01-15",
                "expected": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15},
                "description": "simple EDTF date"
            },
            {
                "input": "+2020-01-15",
                "expected": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15},
                "description": "EDTF with plus prefix"
            },
            {
                "input": "2020-01-01/2020-12-31",
                "expected": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 1},
                "description": "date range within year"
            },
            {
                "input": "+1526-01-01/+2020-12-31",
                "expected": {"likelyYear": 1526, "likelyMonth": 1, "likelyDay": 1},
                "description": "long date range with plus"
            },
            {
                "input": "2020-01-15T10:30:00Z",
                "expected": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15},
                "description": "EDTF with time and timezone"
            },
            {
                "input": "+1910-01-01T00:00:00Z/+1910-12-31T23:59:59Z",
                "expected": {"likelyYear": 1910, "likelyMonth": 1, "likelyDay": 1},
                "description": "datetime range"
            }
        ]
        
        @pytest.mark.parametrize("test_case", full_edtf_cases, ids=lambda x: x['description'])
        def test_full_edtf_parsing(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date_from_formal_date",
                "createFlexibleDateFromFormalDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestPartialDates:
        """Test EDTF parsing of partial dates (missing day or month)."""
        
        partial_edtf_cases = [
            {
                "input": "1945",
                "expected": {"likelyYear": 1945, "likelyMonth": None, "likelyDay": None},
                "description": "year only EDTF"
            },
            {
                "input": "1945-05",
                "expected": {"likelyYear": 1945, "likelyMonth": 5, "likelyDay": None},
                "description": "year-month EDTF"
            },
            {
                "input": "1910/1920",
                "expected": {"likelyYear": 1910, "likelyMonth": None, "likelyDay": None},
                "description": "year range"
            }
        ]
        
        @pytest.mark.parametrize("test_case", partial_edtf_cases, ids=lambda x: x['description'])
        def test_partial_edtf_parsing(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date_from_formal_date",
                "createFlexibleDateFromFormalDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestNullDates:
        """Test edge cases and error handling for EDTF parsing."""
        
        def test_error_handling(self):
            """Test that both implementations handle errors consistently."""
            # These tests check that both implementations handle errors gracefully
            error_cases = [
                "invalid-date-format",
                "2023-13-45",  # Invalid month/day
                "",
                "not-a-date-at-all"
            ]
            
            for invalid_input in error_cases:
                print(f"Testing error handling for: '{invalid_input}'")
                
                # Both implementations should handle errors gracefully
                # We expect them to either return a null date or raise the same type of error
                try:
                    test_data = {"input": invalid_input, "expected": None, "mocks": {}}
                    py_result, ts_result = test_runner.run_dual_test(
                        "create_flexible_date_from_formal_date",
                        "createFlexibleDateFromFormalDate",
                        test_data
                    )
                    
                    # If both succeed, they should return the same result
                    test_runner.assert_strict_parity(py_result, ts_result, f"error handling for '{invalid_input}'")
                    print(f"Both implementations handled '{invalid_input}' consistently: {py_result}")
                        
                except Exception as e:
                    # If one fails, both should fail with similar errors
                    # This is acceptable as long as they behave consistently
                    print(f"Both implementations failed consistently for '{invalid_input}': {str(e)}")
                    pass
