import json
import subprocess
import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Add the FlexibleDate module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'FlexibleDate'))
from FlexibleDate import FlexibleDate, create_flexible_date, create_flexible_date_from_formal_date, compare_two_dates, combine_flexible_dates


class FlexibleDateTestRunner:
    """Test runner that can execute tests against both Python and TypeScript implementations."""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.ts_bridge_path = self.root_dir / "FlexibleDateTS" / "dist" / "test_bridge.js"
        self.test_config_path = self.root_dir / "tests" / "test_config.json"
        
        # Verify TypeScript bridge exists
        if not self.ts_bridge_path.exists():
            raise FileNotFoundError(f"TypeScript bridge not found at {self.ts_bridge_path}")
    
    def load_test_cases(self, test_category: str, test_group: str = None) -> List[Dict[str, Any]]:
        """Load test cases from the JSON configuration file."""
        if not self.test_config_path.exists():
            return []
        
        with open(self.test_config_path, 'r') as f:
            config = json.load(f)
        
        if test_category not in config:
            return []
        
        if test_group is None:
            # Return all test cases in the category
            all_cases = []
            for group in config[test_category].values():
                all_cases.extend(group)
            return all_cases
        else:
            return config[test_category].get(test_group, [])
    
    def serialize_flexible_date(self, fd: FlexibleDate) -> Dict[str, Any]:
        """Convert a Python FlexibleDate to a serializable dictionary."""
        return {
            "likelyYear": fd.likely_year,
            "likelyMonth": fd.likely_month,
            "likelyDay": fd.likely_day
        }
    
    def deserialize_flexible_date(self, data: Dict[str, Any]) -> FlexibleDate:
        """Convert a dictionary back to a Python FlexibleDate."""
        return FlexibleDate(
            likely_year=data.get("likelyYear"),
            likely_month=data.get("likelyMonth"),
            likely_day=data.get("likelyDay")
        )
    
    def run_python_test(self, method: str, *args) -> Any:
        """Execute a test using the Python implementation."""
        try:
            if method == "createFlexibleDate":
                return self.serialize_flexible_date(create_flexible_date(args[0]))
            
            elif method == "createFlexibleDateFromFormalDate":
                return self.serialize_flexible_date(create_flexible_date_from_formal_date(args[0]))
            
            elif method == "compareTwoDates":
                fd1 = self.deserialize_flexible_date(args[0])
                fd2 = self.deserialize_flexible_date(args[1])
                return compare_two_dates(fd1, fd2)
            
            elif method == "combineFlexibleDates":
                dates = [self.deserialize_flexible_date(d) for d in args[0]]
                return self.serialize_flexible_date(combine_flexible_dates(dates))
            
            elif method == "toString":
                fd = self.deserialize_flexible_date(args[0])
                return str(fd)
            
            elif method == "valueOf":
                fd = self.deserialize_flexible_date(args[0])
                return fd.valueOf()
            
            else:
                raise ValueError(f"Unknown method: {method}")
                
        except Exception as e:
            raise RuntimeError(f"Python test failed: {str(e)}")
    
    def run_typescript_test(self, method: str, *args) -> Any:
        """Execute a test using the TypeScript implementation via subprocess."""
        try:
            request = {
                "method": method,
                "args": list(args)
            }
            
            # Call the TypeScript bridge
            result = subprocess.run(
                ["node", str(self.ts_bridge_path), json.dumps(request)],
                capture_output=True,
                text=True,
                cwd=str(self.root_dir)
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"TypeScript bridge failed: {result.stderr}")
            
            response = json.loads(result.stdout)
            
            if not response.get("success", False):
                raise RuntimeError(f"TypeScript test failed: {response.get('error', 'Unknown error')}")
            
            return response["result"]
            
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse TypeScript response: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"TypeScript test failed: {str(e)}")
    
    def compare_results(self, python_result: Any, typescript_result: Any, tolerance: float = 1e-10) -> bool:
        """Compare results from Python and TypeScript implementations."""
        if type(python_result) != type(typescript_result):
            return False
        
        if isinstance(python_result, (int, float)) and isinstance(typescript_result, (int, float)):
            # For numeric results, use tolerance comparison
            return abs(python_result - typescript_result) <= tolerance
        
        elif isinstance(python_result, dict) and isinstance(typescript_result, dict):
            # For FlexibleDate objects (serialized as dicts)
            return (
                python_result.get("likelyYear") == typescript_result.get("likelyYear") and
                python_result.get("likelyMonth") == typescript_result.get("likelyMonth") and
                python_result.get("likelyDay") == typescript_result.get("likelyDay")
            )
        
        else:
            # For other types (strings, booleans, etc.)
            return python_result == typescript_result
    
    def run_dual_test(self, method: str, *args, expected: Any = None) -> bool:
        """Run a test against both implementations and compare results."""
        python_result = self.run_python_test(method, *args)
        typescript_result = self.run_typescript_test(method, *args)
        
        # Compare implementations
        if not self.compare_results(python_result, typescript_result):
            raise AssertionError(
                f"Implementation mismatch for {method}:\n"
                f"Python: {python_result}\n"
                f"TypeScript: {typescript_result}"
            )
        
        # Check expected result if provided
        if expected is not None:
            if not self.compare_results(python_result, expected):
                raise AssertionError(
                    f"Result mismatch for {method}:\n"
                    f"Expected: {expected}\n"
                    f"Got: {python_result}"
                )
        
        return True
