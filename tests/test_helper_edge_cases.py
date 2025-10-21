import pytest
from test_utils import FlexibleDateTestRunner

# Initialize the test runner (will handle environment setup automatically)
test_runner = FlexibleDateTestRunner()


class TestEdgeCases:
    """Test edge cases in date parsing and helper functions."""
    
    class TestAncientDates:
        """Test handling of BC dates and ancient years."""
        
        ancient_date_cases = [
            {
                "input": "-500",
                "expected": {"likelyYear": -500, "likelyMonth": None, "likelyDay": None},
                "description": "BC year with minus sign"
            },
            {
                "input": "500 BC",
                "expected": {"likelyYear": -500, "likelyMonth": None, "likelyDay": None},
                "description": "BC year with BC suffix"
            },
            {
                "input": "0050",
                "expected": {"likelyYear": 50, "likelyMonth": None, "likelyDay": None},
                "description": "year 50 AD with leading zeros"
            },
            {
                "input": "0005",
                "expected": {"likelyYear": 5, "likelyMonth": None, "likelyDay": None},
                "description": "year 5 AD with leading zeros"
            },
            {
                "input": "99",
                "expected": {"likelyYear": 99, "likelyMonth": None, "likelyDay": None},
                "description": "year 99 AD"
            },
            {
                "input": "5",
                "expected": {"likelyYear": 5, "likelyMonth": None, "likelyDay": None},
                "description": "single digit year"
            },
            {
                "input": "-1000",
                "expected": {"likelyYear": -1000, "likelyMonth": None, "likelyDay": None},
                "description": "year 1000 BC"
            },
            {
                "input": "50",
                "expected": {"likelyYear": 50, "likelyMonth": None, "likelyDay": None},
                "description": "year 50 AD (AncientDateTime path)"
            },
            {
                "input": "-50",
                "expected": {"likelyYear": -50, "likelyMonth": None, "likelyDay": None},
                "description": "year 50 BC (AncientDateTime path)"
            }
        ]
        
        @pytest.mark.parametrize("test_case", ancient_date_cases, ids=lambda x: x['description'])
        def test_ancient_dates(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestTextCleaning:
        """Test complex text cleaning scenarios."""
        
        text_cleaning_cases = [
            {
                "input": "2020/05/15",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date with slashes"
            },
            {
                "input": "2020.05.15",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date with dots"
            },
            {
                "input": "2020_05_15",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date with underscores"
            },
            {
                "input": "2020-05-15 14:30:00",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date with time HH:MM:SS"
            },
            {
                "input": "2020-05-15 14:30",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date with time HH:MM"
            },
            {
                "input": "May 15th, 2020",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date with ordinal suffix"
            },
            {
                "input": "15May2020",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date without spaces"
            },
            {
                "input": "  2020-05-15  ",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date with leading/trailing whitespace"
            },
            {
                "input": "9",
                "expected": {"likelyYear": 9, "likelyMonth": None, "likelyDay": None},
                "description": "single digit year (zero-padding)"
            },
            {
                "input": "85",
                "expected": {"likelyYear": 85, "likelyMonth": None, "likelyDay": None},
                "description": "two digit year (zero-padding)"
            },
            {
                "input": "099",
                "expected": {"likelyYear": 99, "likelyMonth": None, "likelyDay": None},
                "description": "three digit year with leading zero (zero-padding)"
            },
            {
                "input": "1000 bc",
                "expected": {"likelyYear": -1000, "likelyMonth": None, "likelyDay": None},
                "description": "year with BC suffix conversion"
            }
        ]
        
        @pytest.mark.parametrize("test_case", text_cleaning_cases, ids=lambda x: x['description'])
        def test_text_cleaning(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestDecadeAndRanges:
        """Test parsing of decades and special formats."""
        
        decade_cases = [
            {
                "input": "1850s",
                "expected": {"likelyYear": 1850, "likelyMonth": None, "likelyDay": None},
                "description": "decade format (1850s)"
            },
            {
                "input": "circa 1920s",
                "expected": {"likelyYear": 1920, "likelyMonth": None, "likelyDay": None},
                "description": "circa with decade"
            },
            {
                "input": "early 1990s",
                "expected": {"likelyYear": 1990, "likelyMonth": None, "likelyDay": None},
                "description": "early with decade"
            },
            {
                "input": "late 2000s",
                "expected": {"likelyYear": 2000, "likelyMonth": None, "likelyDay": None},
                "description": "late with decade"
            }
        ]
        
        @pytest.mark.parametrize("test_case", decade_cases, ids=lambda x: x['description'])
        def test_decades(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestAMPMHandling:
        """Test handling of AM/PM markers in dates."""
        
        ampm_cases = [
            {
                "input": "May 15, 2020 3:00 PM",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date with PM time"
            },
            {
                "input": "May 15, 2020 9:00 AM",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date with AM time"
            },
            {
                "input": "2020-05-15 11:30 pm",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date with lowercase pm"
            }
        ]
        
        @pytest.mark.parametrize("test_case", ampm_cases, ids=lambda x: x['description'])
        def test_ampm_handling(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestSpecialCharacters:
        """Test handling of special characters and quotes."""
        
        special_char_cases = [
            {
                "input": '"May 15, 2020"',
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date in double quotes"
            },
            {
                "input": "'May 15, 2020'",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date in single quotes"
            },
            {
                "input": "May, 15, 2020",
                "expected": {"likelyYear": 2020, "likelyMonth": 5, "likelyDay": 15},
                "description": "date with extra commas"
            }
        ]
        
        @pytest.mark.parametrize("test_case", special_char_cases, ids=lambda x: x['description'])
        def test_special_characters(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestParserEdgeCases:
        """Test edge cases in _parse_with_date_util that trigger fallback to gleaning."""
        
        parser_edge_cases = [
            {
                "input": "0050",
                "expected": {"likelyYear": 50, "likelyMonth": None, "likelyDay": None},
                "description": "year 0050 triggers parser exception, falls back to gleaning"
            },
            {
                "input": "50 bc",
                "expected": {"likelyYear": -50, "likelyMonth": None, "likelyDay": None},
                "description": "BC in input triggers parser exception, falls back to gleaning"
            }
        ]
        
        @pytest.mark.parametrize("test_case", parser_edge_cases, ids=lambda x: x['description'])
        def test_parser_edge_cases(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])
    
    class TestComplexDateGleaning:
        """Test complex date gleaning scenarios with multiple possibilities."""
        
        complex_gleaning_cases = [
            {
                "input": "12 13 2020",
                "expected": {"likelyYear": 2020, "likelyMonth": 12, "likelyDay": 13},
                "description": "ambiguous day/month numbers (exercises substitution logic)"
            }
        ]
        
        @pytest.mark.parametrize("test_case", complex_gleaning_cases, ids=lambda x: x['description'])
        def test_complex_gleaning(self, test_case):
            test_data = {"input": test_case["input"], "expected": test_case["expected"], "mocks": {}}
            
            py_result, ts_result = test_runner.run_dual_test(
                "create_flexible_date",
                "createFlexibleDate",
                test_data
            )
            
            assert py_result == test_case["expected"], f"Python failed for {test_case['description']}"
            assert ts_result == test_case["expected"], f"TypeScript failed for {test_case['description']}"
            test_runner.assert_strict_parity(py_result, ts_result, test_case['description'])

