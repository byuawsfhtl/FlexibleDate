import pytest
from test_utils import FlexibleDateTestRunner


class TestCompareTwoDates:
    """Test date comparison functionality in both Python and TypeScript."""
    
    def setup_method(self):
        """Set up test runner for each test method."""
        self.runner = FlexibleDateTestRunner()
    
    def test_identical_dates(self):
        """Test comparison of identical dates."""
        test_cases = self.runner.load_test_cases("compare_two_dates", "identical")
        
        for case in test_cases:
            print(f"Testing: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "compareTwoDates",
                case["input"][0],
                case["input"][1],
                expected=case["expected"]
            )
    
    def test_similar_dates(self):
        """Test comparison of similar dates."""
        test_cases = self.runner.load_test_cases("compare_two_dates", "similar")
        
        for case in test_cases:
            print(f"Testing: {case['name']}")
            
            # For similar dates, we might have a range of acceptable scores
            py_result = self.runner.run_python_test(
                "compareTwoDates",
                case["input"][0],
                case["input"][1]
            )
            ts_result = self.runner.run_typescript_test(
                "compareTwoDates",
                case["input"][0],
                case["input"][1]
            )
            
            # Ensure both implementations return the same result
            assert self.runner.compare_results(py_result, ts_result), \
                f"Implementation mismatch for {case['name']}: Python={py_result}, TypeScript={ts_result}"
            
            # Check if result is in expected range (if provided)
            if "expected_range" in case:
                min_score, max_score = case["expected_range"]
                assert min_score <= py_result <= max_score, \
                    f"Score {py_result} not in expected range [{min_score}, {max_score}] for {case['name']}"
    
    def test_different_dates(self):
        """Test comparison of very different dates."""
        test_cases = self.runner.load_test_cases("compare_two_dates", "different")
        
        for case in test_cases:
            print(f"Testing: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "compareTwoDates",
                case["input"][0],
                case["input"][1],
                expected=case["expected"]
            )
    
    def test_null_date_comparisons(self):
        """Test comparison involving null/empty dates."""
        null_cases = [
            {
                "name": "both_null",
                "input": [
                    {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                    {"likelyYear": None, "likelyMonth": None, "likelyDay": None}
                ],
                "expected": 100.0
            },
            {
                "name": "one_null_one_valid",
                "input": [
                    {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                    {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
                ],
                "expected": 100.0
            },
            {
                "name": "partial_vs_complete",
                "input": [
                    {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                    {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
                ],
                "expected": 100.0
            }
        ]
        
        for case in null_cases:
            print(f"Testing null case: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "compareTwoDates",
                case["input"][0],
                case["input"][1],
                expected=case["expected"]
            )
    
    def test_edge_case_comparisons(self):
        """Test edge cases in date comparison."""
        edge_cases = [
            {
                "name": "same_month_different_years",
                "input": [
                    {"likelyYear": 1900, "likelyMonth": 5, "likelyDay": None},
                    {"likelyYear": 1901, "likelyMonth": 5, "likelyDay": None}
                ]
            },
            {
                "name": "leap_year_dates",
                "input": [
                    {"likelyYear": 2020, "likelyMonth": 2, "likelyDay": 29},
                    {"likelyYear": 2021, "likelyMonth": 2, "likelyDay": 28}
                ]
            },
            {
                "name": "end_of_year_dates",
                "input": [
                    {"likelyYear": 2019, "likelyMonth": 12, "likelyDay": 31},
                    {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 1}
                ]
            }
        ]
        
        for case in edge_cases:
            print(f"Testing edge case: {case['name']}")
            
            # For edge cases, we just ensure both implementations return the same result
            py_result = self.runner.run_python_test(
                "compareTwoDates",
                case["input"][0],
                case["input"][1]
            )
            ts_result = self.runner.run_typescript_test(
                "compareTwoDates",
                case["input"][0],
                case["input"][1]
            )
            
            assert self.runner.compare_results(py_result, ts_result), \
                f"Implementation mismatch for {case['name']}: Python={py_result}, TypeScript={ts_result}"
