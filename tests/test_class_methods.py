import pytest
from test_utils import FlexibleDateTestRunner

# Initialize the test runner (will handle environment setup automatically)
test_runner = FlexibleDateTestRunner()


class TestBoolMethod:
    """Test the __bool__ method of FlexibleDate."""
    
    bool_test_cases = [
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
            "expected": False,
            "description": "fully null date returns False"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "expected": True,
            "description": "full date returns True"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
            "expected": True,
            "description": "year only returns True"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
            "expected": True,
            "description": "year and month returns True"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": 5, "likelyDay": None},
            "expected": True,
            "description": "month only returns True"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": 15},
            "expected": True,
            "description": "day only returns True"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": 5, "likelyDay": 15},
            "expected": True,
            "description": "month and day returns True"
        }
    ]
    
    # Note: NaN handling test (line 78) cannot be tested via public API
    # since Pydantic validators enforce Optional[int] types, not float.
    # The math.isnan check appears to be defensive programming.
    
    @pytest.mark.parametrize("test_case", bool_test_cases, ids=lambda x: x['description'])
    def test_bool_method(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "test_bool",
            "testBool",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestStrMethod:
    """Test the __str__ method of FlexibleDate."""
    
    str_test_cases = [
        {
            "input": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "expected": "15 May 2020",
            "description": "full date"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
            "expected": "2020",
            "description": "year only"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
            "expected": "May 2020",
            "description": "year and month"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": 5, "likelyDay": 15},
            "expected": "15 May",
            "description": "month and day (no year)"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": 5, "likelyDay": None},
            "expected": "May",
            "description": "month only"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": 15},
            "expected": "15",
            "description": "day only"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
            "expected": "",
            "description": "null date"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": None},
            "expected": "Jan 2020",
            "description": "January abbreviation"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 2, "likelyDay": None},
            "expected": "Feb 2020",
            "description": "February abbreviation"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 3, "likelyDay": None},
            "expected": "Mar 2020",
            "description": "March abbreviation"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 4, "likelyDay": None},
            "expected": "Apr 2020",
            "description": "April abbreviation"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None},
            "expected": "Jun 2020",
            "description": "June abbreviation"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 7, "likelyDay": None},
            "expected": "Jul 2020",
            "description": "July abbreviation"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 8, "likelyDay": None},
            "expected": "Aug 2020",
            "description": "August abbreviation"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 9, "likelyDay": None},
            "expected": "Sep 2020",
            "description": "September abbreviation"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 10, "likelyDay": None},
            "expected": "Oct 2020",
            "description": "October abbreviation"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 11, "likelyDay": None},
            "expected": "Nov 2020",
            "description": "November abbreviation"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 12, "likelyDay": None},
            "expected": "Dec 2020",
            "description": "December abbreviation"
        }
    ]
    
    @pytest.mark.parametrize("test_case", str_test_cases, ids=lambda x: x['description'])
    def test_str_method(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "test_str",
            "testStr",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestReprMethod:
    """Test the __repr__ method of FlexibleDate."""
    
    repr_test_cases = [
        {
            "input": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "expected": "+2020-05-15",
            "description": "full date"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
            "expected": "+2020-05",
            "description": "year and month"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
            "expected": "+2020",
            "description": "year only"
        },
        {
            "input": {"likelyYear": 500, "likelyMonth": None, "likelyDay": None},
            "expected": "+0500",
            "description": "year with padding (3 digits)"
        },
        {
            "input": {"likelyYear": 50, "likelyMonth": None, "likelyDay": None},
            "expected": "+0050",
            "description": "year with padding (2 digits)"
        },
        {
            "input": {"likelyYear": 5, "likelyMonth": None, "likelyDay": None},
            "expected": "+0005",
            "description": "year with padding (1 digit)"
        },
        {
            "input": {"likelyYear": -500, "likelyMonth": None, "likelyDay": None},
            "expected": "-0500",
            "description": "BC date (negative year)"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 5},
            "expected": "+2020-01-05",
            "description": "single digit month and day with padding"
        },
        {
            "input": {"likelyYear": 2020, "likelyMonth": 12, "likelyDay": 31},
            "expected": "+2020-12-31",
            "description": "double digit month and day"
        },
        {
            "input": {"likelyYear": 0, "likelyMonth": None, "likelyDay": None},
            "expected": "0000",
            "description": "year 0"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": 5, "likelyDay": None},
            "expected": "XXXX-05",
            "description": "month only (no year, no day)"
        }
    ]
    
    @pytest.mark.parametrize("test_case", repr_test_cases, ids=lambda x: x['description'])
    def test_repr_method(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "test_repr",
            "testRepr",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

