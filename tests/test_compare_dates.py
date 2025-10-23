import pytest
from test_utils import FlexibleDateTestRunner

# Initialize the test runner (will handle environment setup automatically)
test_runner = FlexibleDateTestRunner()

class TestIdenticalDates:
    """Test comparison of identical dates returns perfect score of 100."""

    test_cases = [
            {
                "input": [
                    {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15},
                    {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15}
                ],
                "expected": 100,
                "description": "identical full dates"
            },
            {
                "input": [
                    {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                    {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None}
                ],
                "expected": 100,
                "description": "identical year-month dates"
            },
            {
                "input": [
                    {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None},
                    {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None}
                ],
                "expected": 100,
                "description": "identical year-only dates"
            }
        ]

    @pytest.mark.parametrize("test_case", test_cases, ids=lambda x: x['description'])
    def test_identical_full_dates(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        py_result, ts_result = test_runner.run_dual_test(
            "compare_two_dates",
            "compareDates",
            test_data
        )
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

    edge_cases = [
            {
                "input": [
                    {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                    {"likelyYear": None, "likelyMonth": None, "likelyDay": None}
                ],
                "expected": 100,
                "description": "both dates completely null"
            },
            {
                "input": [
                    {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                    {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
                ],
                "expected": 100,
                "description": "one null date, one valid date"
            },
            {
                "input": [
                    {"likelyYear": 2020, "likelyMonth": None, "likelyDay": 15},
                    {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None}
                ],
                "expected": 100,
                "description": "no overlapping non-null fields except year"
            }
        ]

    @pytest.mark.parametrize("test_case", edge_cases, ids=lambda x: x['description'])
    def test_edge_cases(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
        py_result, ts_result = test_runner.run_dual_test(
            "compare_two_dates",
            "compareDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

class TestSimilarDates:
    """Test comparison of similar dates."""

    one_day_different_cases = [
            {
                "input": [
                    {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15},
                    {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 16}
                ],
                "expected": 97.77778,
                "description": "1 day difference, same month and year"
            },
            {
                "input": [
                    {"likelyYear": 2020, "likelyMonth": 3, "likelyDay": 10},
                    {"likelyYear": 2020, "likelyMonth": 3, "likelyDay": 13}
                ],
                "expected": 93.33333,
                "description": "3 day difference"
            },
            {
                "input": [
                    {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": 1},
                    {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": 16}
                ],
                "expected": 66.66667,
                "description": "15 day difference (at boundary)"
            }
        ]

    @pytest.mark.parametrize("test_case", one_day_different_cases, ids=lambda x: x['description'])
    def test_one_day_different_cases(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
        py_result, ts_result = test_runner.run_dual_test(
            "compare_two_dates",
            "compareDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

    one_month_different_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None}
            ],
            "expected": 91.66667,
            "description": "1 month difference, year-month dates"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 4, "likelyDay": 15}
            ],
            "expected": 83.33333,
            "description": "3 month difference, same day and year"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 7, "likelyDay": None}
            ],
            "expected": 50,
            "description": "6 month difference (at boundary)"
        }
    ]

    @pytest.mark.parametrize("test_case", one_month_different_cases, ids=lambda x: x['description'])
    def test_one_month_different_cases(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
        py_result, ts_result = test_runner.run_dual_test(
            "compare_two_dates",
            "compareDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

    one_year_different_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2021, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": 95,
            "description": "1 year difference, year-only dates"
        },
        {
            "input": [
                {"likelyYear": 2015, "likelyMonth": 5, "likelyDay": 10},
                {"likelyYear": 2016, "likelyMonth": 5, "likelyDay": 10}
            ],
            "expected": 98.33333,
            "description": "1 year difference, same month and day"
        }
    ]

    @pytest.mark.parametrize("test_case", one_year_different_cases, ids=lambda x: x['description'])
    def test_one_year_different_cases(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
        py_result, ts_result = test_runner.run_dual_test(
            "compare_two_dates",
            "compareDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

    year_only_five_years_different_cases = [
        {
            "input": [
                {"likelyYear": 1990, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": 75,
            "description": "5 year difference, year-only dates"
        },
        {
            "input": [
                {"likelyYear": 2000, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2005, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": 75,
            "description": "5 year difference forward"
        },
        {
            "input": [
                {"likelyYear": 2010, "likelyMonth": 6, "likelyDay": None},
                {"likelyYear": 2015, "likelyMonth": 6, "likelyDay": None}
            ],
            "expected": 87.5,
            "description": "5 year difference with same month"
        }
    ]

    @pytest.mark.parametrize("test_case", year_only_five_years_different_cases, ids=lambda x: x['description'])
    def test_year_only_five_years_different_cases(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
        py_result, ts_result = test_runner.run_dual_test(
            "compare_two_dates",
            "compareDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

    partial_date_comparisons_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None}
            ],
            "expected": 100,
            "description": "full date vs year-month (matching fields)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": 100,
            "description": "year-only vs full date (matching year)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2025, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": 75,
            "description": "year-only vs full date (5 year diff)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 3, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": 15}
            ],
            "expected": 75,
            "description": "year-month vs full date (3 month diff)"
        }
    ]

    @pytest.mark.parametrize("test_case", partial_date_comparisons_cases, ids=lambda x: x['description'])
    def test_partial_date_comparisons_cases(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
        py_result, ts_result = test_runner.run_dual_test(
            "compare_two_dates",
            "compareDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

    scoring_boundaries_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 1},
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 15}
            ],
            "expected": 68.88889,
            "description": "14 day difference (near boundary)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 1},
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 16}
            ],
            "expected": 66.66667,
            "description": "15 day difference (at max_diff boundary)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 1},
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 20}
            ],
            "expected": 66.66667,
            "description": "19 day difference (beyond max_diff)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None}
            ],
            "expected": 58.33333,
            "description": "5 month difference (near boundary)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2039, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": 5,
            "description": "19 year difference (just before boundary)"
        },
        {
            "input": [
                {"likelyYear": 2000, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2010, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": 50,
            "description": "10 year difference (halfway to boundary)"
        }
    ]

    @pytest.mark.parametrize("test_case", scoring_boundaries_cases, ids=lambda x: x['description'])
    def test_scoring_boundaries_cases(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
        py_result, ts_result = test_runner.run_dual_test(
            "compare_two_dates",
            "compareDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}: got {py_result}, expected {test_case['expected']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}: got {ts_result}, expected {test_case['expected']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestBadDates:
    """Test comparison of dates that are too different (score = 0)."""

    very_different_dates_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2040, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": 0,
            "description": "20 year difference (at boundary)"
        },
        {
            "input": [
                {"likelyYear": 1990, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": 0,
            "description": "30 year difference with same month and day"
        },
        {
            "input": [
                {"likelyYear": 1950, "likelyMonth": 1, "likelyDay": 1},
                {"likelyYear": 2024, "likelyMonth": 12, "likelyDay": 31}
            ],
            "expected": 0,
            "description": "very different dates in all fields"
        },
        {
            "input": [
                {"likelyYear": 1800, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 1900, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": 0,
            "description": "100 year difference"
        }
    ]

    @pytest.mark.parametrize("test_case", very_different_dates_cases, ids=lambda x: x['description'])
    def test_very_different_dates_cases(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
        py_result, ts_result = test_runner.run_dual_test(
            "compare_two_dates",
            "compareDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])