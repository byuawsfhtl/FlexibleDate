import pytest
from pathlib import Path
from pyscripttestutils import PyScriptTestRunner
from FlexibleDate.FlexibleDate import FlexibleDate

runner = PyScriptTestRunner(
    Path(__file__).resolve().parent.parent / "FlexibleDateTS" / "dist" / "test_bridge.js",
    deserializer = lambda d: FlexibleDate(likely_day=d["likelyDay"], likely_month=d["likelyMonth"], likely_year=d["likelyYear"]),
)

runner.add_method(FlexibleDate.create_flexible_date, "createFlexibleDate")
runner.add_method(FlexibleDate.create_flexible_date_from_formal_date, "createFlexibleDateFromFormalDate")

class TestCreateFlexibleDate:
    """Test FlexibleDate creation from string inputs in both Python and TypeScript."""
    
    class TestFullDates:
        """Test parsing of complete dates with year, month, and day."""
        
        full_date_cases = [
            {
                "input": "2023-05-15",
                "expected": FlexibleDate(likely_day=15, likely_month=5, likely_year=2023),
                "description": "ISO format"
            },
            {
                "input": "January 15, 2020",
                "expected": FlexibleDate(likely_day=15, likely_month=1, likely_year=2020),
                "description": "American format with comma"
            },
            {
                "input": "15 January 2020",
                "expected": FlexibleDate(likely_day=15, likely_month=1, likely_year=2020),
                "description": "European format"
            },
            {
                "input": "2020-01-15",
                "expected": FlexibleDate(likely_day=15, likely_month=1, likely_year=2020),
                "description": "ISO format dash separated"
            },
            {
                "input": "01/15/2020",
                "expected": FlexibleDate(likely_day=15, likely_month=1, likely_year=2020),
                "description": "MM/DD/YYYY format"
            },
            {
                "input": "15/01/2020",
                "expected": FlexibleDate(likely_day=15, likely_month=1, likely_year=2020),
                "description": "DD/MM/YYYY format"
            },
            {
                "input": "Born on March 15, 1990 in New York",
                "expected": FlexibleDate(likely_day=15, likely_month=3, likely_year=1990),
                "description": "date embedded in text"
            },
            {
                "input": "1990, 1991, or 1992",
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=1991),
                "description": "multiple 4-digit years (tests glean_year_month_day scoring)"
            }
        ]
        
        @pytest.mark.parametrize("test_case", full_date_cases, ids=lambda x: x['description'])
        def test_full_date_parsing(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = runner.run(
                "FlexibleDate.create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestPartialDates:
        """Test parsing of partial dates (missing day, month, or both)."""
        
        partial_date_cases = [
            {
                "input": "May 2023",
                "expected": FlexibleDate(likely_day=None, likely_month=5, likely_year=2023),
                "description": "month and year only"
            },
            {
                "input": "1995",
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=1995),
                "description": "year only"
            },
            {
                "input": "December",
                "expected": FlexibleDate(likely_day=None, likely_month=12, likely_year=None),
                "description": "month only"
            },
            {
                "input": "December 12",
                "expected": FlexibleDate(likely_day=12, likely_month=12, likely_year=None),
                "description": "month and day only"
            },
            {
                "input": "The event happened sometime in July 2021",
                "expected": FlexibleDate(likely_day=None, likely_month=7, likely_year=2021),
                "description": "month and year in sentence"
            },
            {
                "input": "circa 1850s",
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=1850),
                "description": "approximate year with text"
            }
        ]
        
        @pytest.mark.parametrize("test_case", partial_date_cases, ids=lambda x: x['description'])
        def test_partial_date_parsing(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = runner.run(
                "FlexibleDate.create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestNullDates:
        """Test handling of null and empty inputs."""
        
        null_date_cases = [
            {
                "input": None,
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=None),
                "description": "null input"
            },
            {
                "input": "",
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=None),
                "description": "empty string"
            },
            {
                "input": "   ",
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=None),
                "description": "whitespace only"
            }
        ]
        
        @pytest.mark.parametrize("test_case", null_date_cases, ids=lambda x: x['description'])
        def test_null_and_empty_inputs(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = runner.run(
                "FlexibleDate.create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestInvalidDatesExceptionHandling:
        """Test handling of invalid dates that trigger exception handling."""
        
        invalid_date_cases = [
            {
                "input": "February 30, 2020",
                "expected": FlexibleDate(likely_day=None, likely_month=2, likely_year=2020),
                "description": "February 31st (invalid) falls back to year-month"
            },
            {
                "input": "April 31, 2020",
                "expected": FlexibleDate(likely_day=None, likely_month=4, likely_year=2020),
                "description": "April 31st (invalid) falls back to year-month"
            },
            {
                "input": "June 31, 2020",
                "expected": FlexibleDate(likely_day=None, likely_month=6, likely_year=2020),
                "description": "June 31st (invalid) falls back to year-month"
            }
        ]
        
        @pytest.mark.parametrize("test_case", invalid_date_cases, ids=lambda x: x['description'])
        def test_invalid_date_exception_handling(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = runner.run(
                "FlexibleDate.create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestCreateFlexibleDateFromFormalDate:
    """Test FlexibleDate creation from EDTF format strings in both Python and TypeScript."""
    
    class TestFullDates:
        """Test EDTF parsing of complete dates with year, month, and day."""
        
        full_edtf_cases = [
            {
                "input": "2020-01-15",
                "expected": FlexibleDate(likely_day=15, likely_month=1, likely_year=2020),
                "description": "simple EDTF date"
            },
            {
                "input": "+2020-01-15",
                "expected": FlexibleDate(likely_day=15, likely_month=1, likely_year=2020),
                "description": "EDTF with plus prefix"
            },
            {
                "input": "2020-01-01/2020-12-31",
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=2020),
                "description": "date range within year"
            },
            {
                "input": "+1526-01-01/+2020-12-31",
                "expected": FlexibleDate(likely_day=1, likely_month=1, likely_year=1526),
                "description": "long date range with plus"
            },
            {
                "input": "2020-01-15T10:30:00Z",
                "expected": FlexibleDate(likely_day=15, likely_month=1, likely_year=2020),
                "description": "EDTF with time and timezone"
            },
            {
                "input": "+1910-01-01T00:00:00Z/+1910-12-31T23:59:59Z",
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=1910),
                "description": "datetime range"
            }
        ]
        
        @pytest.mark.parametrize("test_case", full_edtf_cases, ids=lambda x: x['description'])
        def test_full_edtf_parsing(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = runner.run(
                "FlexibleDate.create_flexible_date_from_formal_date",
                "createFlexibleDateFromFormalDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestPartialDates:
        """Test EDTF parsing of partial dates (missing day or month)."""
        
        partial_edtf_cases = [
            {
                "input": "1945",
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=1945),
                "description": "year only EDTF"
            },
            {
                "input": "1945-05",
                "expected": FlexibleDate(likely_day=None, likely_month=5, likely_year=1945),
                "description": "year-month EDTF"
            },
            {
                "input": "1910/1920",
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=1910),
                "description": "year range"
            },
            {
                "input": "+1945",
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=1945),
                "description": "year only with plus prefix"
            },
            {
                "input": "A+1850",
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=1850),
                "description": "year only with plus prefix and text"
            },
            {
                "input": '+1953-01/+1953-12',
                "expected": FlexibleDate(likely_day=None, likely_month=None, likely_year=1953),
                "description": "full year as month range"
            }
        ]
        
        @pytest.mark.parametrize("test_case", partial_edtf_cases, ids=lambda x: x['description'])
        def test_partial_edtf_parsing(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = runner.run(
                "FlexibleDate.create_flexible_date_from_formal_date",
                "createFlexibleDateFromFormalDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestNullDates:
        """Test edge cases and error handling for EDTF parsing."""
        error_cases = [
            {
                "input": "invalid-date-format",
                "expected": {"error": True},
                "expected_error": True,
                "description": "invalid date format"
            },
            {
                "input": "2023-13-45",
                "expected": {"error": True},
                "expected_error": True,
                "description": "invalid month/day"
            }
        ]
        
        @pytest.mark.parametrize("test_case", error_cases, ids=lambda x: x['description'])
        def test_error_handling(self, test_case):
            """Test that both implementations handle errors consistently."""
            test_data = {
                "input": test_case["input"],
                "expected": test_case["expected"],
                "expected_error": test_case["expected_error"],
                "mocks": {}
            }
            py_result, ts_result = runner.run(
                "FlexibleDate.create_flexible_date_from_formal_date",
                "createFlexibleDateFromFormalDate",
                test_data
            )
            
            # Both should return error dicts with error=True
            assert isinstance(py_result, dict) and py_result.get("error") is True, \
                f"Python should raise error for {test_case['description']}, got: {py_result}"
            assert isinstance(ts_result, dict) and ts_result.get("error") is True, \
                f"TypeScript should raise error for {test_case['description']}, got: {ts_result}"