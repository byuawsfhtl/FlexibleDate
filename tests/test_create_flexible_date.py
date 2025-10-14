import pytest
from test_utils import FlexibleDateTestRunner


class TestCreateFlexibleDate:
    """Test FlexibleDate creation from string inputs in both Python and TypeScript."""
    
    def setup_method(self):
        """Set up test runner for each test method."""
        self.runner = FlexibleDateTestRunner()
    
    def test_basic_date_creation(self):
        """Test basic date string parsing."""
        test_cases = self.runner.load_test_cases("create_flexible_date", "basic")
        
        for case in test_cases:
            print(f"Testing: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "createFlexibleDate",
                case["input"],
                expected=case["expected"]
            )
    
    def test_messy_date_creation(self):
        """Test parsing of messy/dirty date strings."""
        test_cases = self.runner.load_test_cases("create_flexible_date", "messy_dates")
        
        for case in test_cases:
            print(f"Testing: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "createFlexibleDate",
                case["input"],
                expected=case["expected"]
            )
    
    def test_edge_cases(self):
        """Test edge cases for date creation."""
        edge_cases = [
            {
                "name": "very_old_date",
                "input": "1066",
                "expected": {
                    "likelyYear": 1066,
                    "likelyMonth": None,
                    "likelyDay": None
                }
            },
            {
                "name": "future_date",
                "input": "2050-12-31",
                "expected": {
                    "likelyYear": 2050,
                    "likelyMonth": 12,
                    "likelyDay": 31
                }
            }
        ]
        
        for case in edge_cases:
            print(f"Testing edge case: {case['name']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "createFlexibleDate",
                case["input"],
                expected=case["expected"]
            )
    
    def test_string_representation(self):
        """Test string representation of FlexibleDate objects."""
        # Test cases with known string outputs
        test_data = [
            {
                "fd_data": {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15},
                "expected": "15 May 2023"
            },
            {
                "fd_data": {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": None},
                "expected": "May 2023"
            },
            {
                "fd_data": {"likelyYear": 2023, "likelyMonth": None, "likelyDay": None},
                "expected": "2023"
            },
            {
                "fd_data": {"likelyYear": None, "likelyMonth": 5, "likelyDay": 15},
                "expected": "15 May"
            }
        ]
        
        for case in test_data:
            print(f"Testing string representation: {case['fd_data']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "toString",
                case["fd_data"],
                expected=case["expected"]
            )
    
    def test_value_of(self):
        """Test valueOf method (checks if date is not null)."""
        test_data = [
            {
                "fd_data": {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15},
                "expected": True
            },
            {
                "fd_data": {"likelyYear": None, "likelyMonth": None, "likelyDay": None},
                "expected": False
            },
            {
                "fd_data": {"likelyYear": 2023, "likelyMonth": None, "likelyDay": None},
                "expected": True
            }
        ]
        
        for case in test_data:
            print(f"Testing valueOf: {case['fd_data']}")
            
            # Run the test against both implementations
            self.runner.run_dual_test(
                "valueOf",
                case["fd_data"],
                expected=case["expected"]
            )
