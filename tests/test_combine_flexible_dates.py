import pytest
from test_utils import FlexibleDateTestRunner

# Initialize the test runner (will handle environment setup automatically)
test_runner = FlexibleDateTestRunner()


class TestBasicCombining:
    """Test fundamental combining operations."""

    basic_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "single full date"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "two identical full dates"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "three identical full dates"
        },
        {
            "input": [
                {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None},
            "description": "two identical year-only dates"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 7, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 7, "likelyDay": None},
            "description": "single year-month date"
        }
    ]

    @pytest.mark.parametrize("test_case", basic_cases, ids=lambda x: x['description'])
    def test_basic_combining(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "combine_flexible_dates",
            "combineFlexibleDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestConsensus:
    """Test when all or most dates agree."""

    perfect_consensus_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "four dates all agree on all fields"
        },
        {
            "input": [
                {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None},
            "description": "three dates all agree on year only"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
            "description": "three dates all agree on year and month"
        }
    ]

    @pytest.mark.parametrize("test_case", perfect_consensus_cases, ids=lambda x: x['description'])
    def test_perfect_consensus(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "combine_flexible_dates",
            "combineFlexibleDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

    majority_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2021, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "3 of 4 agree on year (strong majority)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "2 of 3 agree on month"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 16}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "4 of 5 agree on day (overwhelming majority)"
        },
        {
            "input": [
                {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 1996, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": 1995, "likelyMonth": None, "likelyDay": None},
            "description": "2 of 3 agree on year-only dates"
        }
    ]

    @pytest.mark.parametrize("test_case", majority_cases, ids=lambda x: x['description'])
    def test_majority_agreement(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "combine_flexible_dates",
            "combineFlexibleDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestProximityScoring:
    """Test the confidence scoring with nearby values."""

    proximity_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2021, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "two years 1 apart (proximity effect, first wins tie)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "two months 1 apart (proximity effect, first wins tie)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 16}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "two days 1 apart (proximity effect, first wins tie)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2021, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2030, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2021, "likelyMonth": None, "likelyDay": None},
            "description": "close years get proximity bonus (2020-2021 closer than 2030)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 12, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None},
            "description": "close months get proximity bonus (5-6 closer than 12)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 16},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 30}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 16},
            "description": "close days get proximity bonus (15-16 closer than 30)"
        }
    ]

    @pytest.mark.parametrize("test_case", proximity_cases, ids=lambda x: x['description'])
    def test_proximity_scoring(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "combine_flexible_dates",
            "combineFlexibleDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestPartialDates:
    """Test combining dates with null fields."""

    partial_date_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "full date with year-only date (non-null wins)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "full date with year-month date (non-null day wins)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
            "description": "year-only with year-month (non-null month wins)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 16},
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "two full dates with one year-only (consensus on non-nulls)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
            "description": "two year-month with one year-only (month from non-nulls)"
        },
        {
            "input": [
                {"likelyYear": None, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "complementary nulls (each field from non-null)"
        }
    ]

    @pytest.mark.parametrize("test_case", partial_date_cases, ids=lambda x: x['description'])
    def test_partial_dates(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "combine_flexible_dates",
            "combineFlexibleDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestNullValues:
    """Test null handling."""

    null_cases = [
        {
            "input": [
                {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": None, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
            "description": "all fields null across all dates"
        },
        {
            "input": [
                {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "one fully null, one with values"
        },
        {
            "input": [
                {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "two fully null, one with values"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2021, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
            "description": "month and day null across all dates"
        },
        {
            "input": [
                {"likelyYear": None, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": None, "likelyMonth": 6, "likelyDay": 16}
            ],
            "expected": {"likelyYear": None, "likelyMonth": 5, "likelyDay": 15},
            "description": "year null across all dates"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 7, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None},
            "description": "day null across all dates"
        }
    ]

    @pytest.mark.parametrize("test_case", null_cases, ids=lambda x: x['description'])
    def test_null_values(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "combine_flexible_dates",
            "combineFlexibleDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestTieBreaking:
    """Test scenarios where confidence scores might be equal."""

    tie_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2021, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "even split 1 vs 1 on year (proximity/first wins)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2021, "likelyMonth": 6, "likelyDay": 16},
                {"likelyYear": 2021, "likelyMonth": 6, "likelyDay": 16}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "even split 2 vs 2 (proximity/first group wins)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2021, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2022, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2021, "likelyMonth": None, "likelyDay": None},
            "description": "three-way tie (proximity cluster wins)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 12, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None},
            "description": "three-way tie on months (proximity effect)"
        }
    ]

    @pytest.mark.parametrize("test_case", tie_cases, ids=lambda x: x['description'])
    def test_tie_breaking(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "combine_flexible_dates",
            "combineFlexibleDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestMixedPrecision:
    """Test combining dates at different levels of precision."""

    mixed_precision_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "year-only + year-month + full date (each field resolved)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "two year-only with one full date"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 16},
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "two full dates with two year-only (fields independent)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "year-month dates with different month consensus"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": 2021, "likelyMonth": 5, "likelyDay": None},
                {"likelyYear": 2022, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2021, "likelyMonth": 5, "likelyDay": 15},
            "description": "different years, month appears twice, day once"
        }
    ]

    @pytest.mark.parametrize("test_case", mixed_precision_cases, ids=lambda x: x['description'])
    def test_mixed_precision(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "combine_flexible_dates",
            "combineFlexibleDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])


class TestEdgeCases:
    """Test boundary conditions and edge cases."""

    edge_cases = [
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 12, "likelyDay": 31},
                {"likelyYear": 2020, "likelyMonth": 12, "likelyDay": 30}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 12, "likelyDay": 31},
            "description": "end of year dates"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 2, "likelyDay": 29},
                {"likelyYear": 2020, "likelyMonth": 2, "likelyDay": 28}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 2, "likelyDay": 29},
            "description": "leap year date"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 1},
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 2}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": 1},
            "description": "start of year dates"
        },
        {
            "input": [
                {"likelyYear": 1850, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 1850, "likelyMonth": 5, "likelyDay": 15},
            "description": "ancient and modern dates"
        },
        {
            "input": [
                {"likelyYear": -500, "likelyMonth": None, "likelyDay": None},
                {"likelyYear": -499, "likelyMonth": None, "likelyDay": None}
            ],
            "expected": {"likelyYear": -500, "likelyMonth": None, "likelyDay": None},
            "description": "BC dates"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
            "description": "many identical dates (10 dates)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 16},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 17},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 18},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 19},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 20}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 17},
            "description": "six consecutive days (proximity clustering)"
        },
        {
            "input": [
                {"likelyYear": 2020, "likelyMonth": 1, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 2, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 3, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 4, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": None},
                {"likelyYear": 2020, "likelyMonth": 6, "likelyDay": None}
            ],
            "expected": {"likelyYear": 2020, "likelyMonth": 3, "likelyDay": None},
            "description": "six consecutive months (proximity clustering)"
        }
    ]

    @pytest.mark.parametrize("test_case", edge_cases, ids=lambda x: x['description'])
    def test_edge_cases(self, test_case):
        test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
        
        py_result, ts_result = test_runner.run_dual_test(
            "combine_flexible_dates",
            "combineFlexibleDates",
            test_data
        )
        
        assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
        assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
        test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

