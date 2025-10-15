import pytest
from test_utils import FlexibleDateTestRunner

# Initialize the test runner (will handle environment setup automatically)
test_runner = FlexibleDateTestRunner()


class TestYearValidator:
    """Test the validate_likely_year validator."""
    
    valid_year_cases = [
        {
            "input": {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
            "expected": {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
            "description": "valid positive year"
        },
        {
            "input": {"likelyYear": -500, "likelyMonth": None, "likelyDay": None},
            "expected": {"likelyYear": -500, "likelyMonth": None, "likelyDay": None},
            "description": "valid negative year (BC)"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
            "expected": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
            "description": "None value accepted"
        },
        {
            "input": {"likelyYear": -100000, "likelyMonth": None, "likelyDay": None},
            "expected": {"likelyYear": -100000, "likelyMonth": None, "likelyDay": None},
            "description": "boundary value -100,000"
        },
        {
            "input": {"likelyYear": 100000, "likelyMonth": None, "likelyDay": None},
            "expected": {"likelyYear": 100000, "likelyMonth": None, "likelyDay": None},
            "description": "boundary value 100,000"
        },
        {
            "input": {"likelyYear": 0, "likelyMonth": None, "likelyDay": None},
            "expected": {"likelyYear": 0, "likelyMonth": None, "likelyDay": None},
            "description": "year zero"
        }
    ]
    
    @pytest.mark.parametrize("test_case", valid_year_cases, ids=lambda x: x['description'])
    def test_valid_years(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "test_validator",
            "testValidator",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    invalid_year_cases = [
        {
            "input": {"likelyYear": -100001, "likelyMonth": None, "likelyDay": None},
            "description": "year below -100,000"
        },
        {
            "input": {"likelyYear": 100001, "likelyMonth": None, "likelyDay": None},
            "description": "year above 100,000"
        },
        {
            "input": {"likelyYear": -500000, "likelyMonth": None, "likelyDay": None},
            "description": "very large negative year"
        },
        {
            "input": {"likelyYear": 500000, "likelyMonth": None, "likelyDay": None},
            "description": "very large positive year"
        }
    ]
    
    @pytest.mark.parametrize("test_case", invalid_year_cases, ids=lambda x: x['description'])
    def test_invalid_years(self, test_case):
        test_data = {"input": test_case["input"], "expected": "ValueError", "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "test_validator",
            "testValidator",
            test_data
        )
        
        assert py_result == "ValueError", f"Python should raise ValueError for {test_case['description']}"
        assert ts_result == "ValueError", f"TypeScript should raise ValueError for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestMonthValidator:
    """Test the validate_likely_month validator."""
    
    valid_month_cases = [
        {
            "input": {"likelyYear": None, "likelyMonth": 1, "likelyDay": None},
            "expected": {"likelyYear": None, "likelyMonth": 1, "likelyDay": None},
            "description": "valid month 1"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": 6, "likelyDay": None},
            "expected": {"likelyYear": None, "likelyMonth": 6, "likelyDay": None},
            "description": "valid month 6"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": 12, "likelyDay": None},
            "expected": {"likelyYear": None, "likelyMonth": 12, "likelyDay": None},
            "description": "valid month 12"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
            "expected": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
            "description": "None value accepted"
        }
    ]
    
    @pytest.mark.parametrize("test_case", valid_month_cases, ids=lambda x: x['description'])
    def test_valid_months(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "test_validator",
            "testValidator",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    invalid_month_cases = [
        {
            "input": {"likelyYear": None, "likelyMonth": 0, "likelyDay": None},
            "description": "month = 0"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": 13, "likelyDay": None},
            "description": "month = 13"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": -1, "likelyDay": None},
            "description": "month = -1"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": 100, "likelyDay": None},
            "description": "month = 100"
        }
    ]
    
    @pytest.mark.parametrize("test_case", invalid_month_cases, ids=lambda x: x['description'])
    def test_invalid_months(self, test_case):
        test_data = {"input": test_case["input"], "expected": "ValueError", "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "test_validator",
            "testValidator",
            test_data
        )
        
        assert py_result == "ValueError", f"Python should raise ValueError for {test_case['description']}"
        assert ts_result == "ValueError", f"TypeScript should raise ValueError for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestDayValidator:
    """Test the validate_likely_day validator."""
    
    valid_day_cases = [
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": 1},
            "expected": {"likelyYear": None, "likelyMonth": None, "likelyDay": 1},
            "description": "valid day 1"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": 15},
            "expected": {"likelyYear": None, "likelyMonth": None, "likelyDay": 15},
            "description": "valid day 15"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": 31},
            "expected": {"likelyYear": None, "likelyMonth": None, "likelyDay": 31},
            "description": "valid day 31"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
            "expected": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
            "description": "None value accepted"
        }
    ]
    
    @pytest.mark.parametrize("test_case", valid_day_cases, ids=lambda x: x['description'])
    def test_valid_days(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "test_validator",
            "testValidator",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    invalid_day_cases = [
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": 0},
            "description": "day = 0"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": 32},
            "description": "day = 32"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": -1},
            "description": "day = -1"
        },
        {
            "input": {"likelyYear": None, "likelyMonth": None, "likelyDay": 100},
            "description": "day = 100"
        }
    ]
    
    @pytest.mark.parametrize("test_case", invalid_day_cases, ids=lambda x: x['description'])
    def test_invalid_days(self, test_case):
        test_data = {"input": test_case["input"], "expected": "ValueError", "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "test_validator",
            "testValidator",
            test_data
        )
        
        assert py_result == "ValueError", f"Python should raise ValueError for {test_case['description']}"
        assert ts_result == "ValueError", f"TypeScript should raise ValueError for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

