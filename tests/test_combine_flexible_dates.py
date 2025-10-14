import pytest
from test_utils import FlexibleDateTestRunner


class TestCombineFlexibleDates:
    """Test date combination functionality in both Python and TypeScript."""
    
    def setup_method(self):
        """Set up test runner for each test method."""
        self.runner = FlexibleDateTestRunner()
    
    def test_basic_date_combination(self):
        """Test basic date combination scenarios."""
        test_cases = self.runner.load_test_cases("combine_flexible_dates", "basic")
        
        for case in test_cases:
            print(f"Testing: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "combineFlexibleDates",
                case["input"][0],  # The array of dates to combine
                expected=case["expected"]
            )
    
    def test_conflicting_dates_combination(self):
        """Test combination of dates with conflicting information."""
        conflicting_cases = [
            {
                "name": "different_years_same_month_day",
                "input": [
                    [
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                        {"likelyYear": 2021, "likelyMonth": 5, "likelyDay": 15},
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
                    ]
                ],
                "expected": {
                    "likelyYear": 2020,  # Most common year should win
                    "likelyMonth": 5,
                    "likelyDay": 15
                }
            },
            {
                "name": "different_months_same_year",
                "input": [
                    [
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                        {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None},
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None}
                    ]
                ],
                "expected": {
                    "likelyYear": 2020,
                    "likelyMonth": 5,  # Most common month should win
                    "likelyDay": None
                }
            },
            {
                "name": "mixed_precision_dates",
                "input": [
                    [
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                        {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None}
                    ]
                ],
                "expected": {
                    "likelyYear": 2020,
                    "likelyMonth": 5,
                    "likelyDay": 15
                }
            }
        ]
        
        for case in conflicting_cases:
            print(f"Testing conflicting case: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "combineFlexibleDates",
                case["input"][0],
                expected=case["expected"]
            )
    
    def test_single_date_combination(self):
        """Test combination of a single date (should return the same date)."""
        single_date_cases = [
            {
                "name": "single_complete_date",
                "input": [
                    [{"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}]
                ],
                "expected": {
                    "likelyYear": 2020,
                    "likelyMonth": 5,
                    "likelyDay": 15
                }
            },
            {
                "name": "single_partial_date",
                "input": [
                    [{"likelyYear": 2020, "likelyMonth": None, "likelyDay": None}]
                ],
                "expected": {
                    "likelyYear": 2020,
                    "likelyMonth": None,
                    "likelyDay": None
                }
            }
        ]
        
        for case in single_date_cases:
            print(f"Testing single date case: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "combineFlexibleDates",
                case["input"][0],
                expected=case["expected"]
            )
    
    def test_empty_and_null_combinations(self):
        """Test combination of empty or null dates."""
        null_cases = [
            {
                "name": "all_null_dates",
                "input": [
                    [
                        {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                        {"likelyYear": None, "likelyMonth": None, "likelyDay": None}
                    ]
                ],
                "expected": {
                    "likelyYear": None,
                    "likelyMonth": None,
                    "likelyDay": None
                }
            },
            {
                "name": "mix_null_and_valid",
                "input": [
                    [
                        {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                        {"likelyYear": None, "likelyMonth": None, "likelyDay": None}
                    ]
                ],
                "expected": {
                    "likelyYear": 2020,
                    "likelyMonth": 5,
                    "likelyDay": 15
                }
            }
        ]
        
        for case in null_cases:
            print(f"Testing null case: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "combineFlexibleDates",
                case["input"][0],
                expected=case["expected"]
            )
    
    def test_large_date_sets(self):
        """Test combination of larger sets of dates."""
        large_set_cases = [
            {
                "name": "many_similar_dates",
                "input": [
                    [
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 16},
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 14},
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                        {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
                    ]
                ],
                "expected": {
                    "likelyYear": 2020,
                    "likelyMonth": 5,
                    "likelyDay": 15  # Most common day should win
                }
            }
        ]
        
        for case in large_set_cases:
            print(f"Testing large set case: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "combineFlexibleDates",
                case["input"][0],
                expected=case["expected"]
            )
