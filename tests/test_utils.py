import json
import subprocess
import sys
import os
import threading
from pathlib import Path
from typing import Any, Dict, Optional
from unittest.mock import patch, MagicMock
import threading


# Add the FlexibleDate module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'FlexibleDate'))
from FlexibleDate import FlexibleDate, create_flexible_date, create_flexible_date_from_formal_date, compare_two_dates, combine_flexible_dates
from pydantic import ValidationError as PydanticValidationError


class FlexibleDateTestRunner:
    """Self-contained test runner for dual-language FlexibleDate testing."""
    
    _environment_initialized = False
    _setup_lock = threading.Lock()
    
    def __init__(self):
        """Initialize the test runner with automatic environment setup."""
        self.root_dir = Path(__file__).parent.parent
        self.ts_bridge_path = self.root_dir / "FlexibleDateTS" / "dist" / "test_bridge.js"
        
        with FlexibleDateTestRunner._setup_lock:
            if not FlexibleDateTestRunner._environment_initialized:
                self._setup_environment()
                FlexibleDateTestRunner._environment_initialized = True
    
    def _setup_environment(self):
        """One-time setup of Node.js environment and TypeScript compilation."""
        print("Setting up dual-language testing environment...")
        
        # Check if TypeScript bridge exists
        if not self.ts_bridge_path.exists():
            # Only check Node.js if we need to compile
            if not self._check_nodejs():
                raise EnvironmentError(
                    "Node.js not found and TypeScript bridge not compiled. Install Node.js to run dual-language tests.\n"
                    "Download from: https://nodejs.org/"
                )
            self._compile_typescript()
        else:
            print("TypeScript bridge found, skipping compilation.")
        
        print("Environment setup complete.")
    
    def _check_nodejs(self) -> bool:
        """Check if Node.js is available."""
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _check_typescript_compiled(self) -> bool:
        """Check if TypeScript bridge is compiled and up-to-date."""
        ts_source = self.root_dir / "FlexibleDateTS" / "test_bridge.ts"
        js_output = self.ts_bridge_path
        
        if not js_output.exists():
            return False
        
        # Check if source is newer than compiled output
        if ts_source.exists() and ts_source.stat().st_mtime > js_output.stat().st_mtime:
            return False
        
        return True
    
    def _compile_typescript(self):
        """Compile TypeScript code."""
        ts_dir = self.root_dir / "FlexibleDateTS"
        
        try:
            print("Installing TypeScript dependencies...")
            result = subprocess.run(['npm', 'ci'], 
                                  cwd=str(ts_dir), 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Failed to install npm dependencies: {result.stderr}")
            
            print("Compiling TypeScript...")
            result = subprocess.run(['npm', 'run', 'build'], 
                                  cwd=str(ts_dir), 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Failed to compile TypeScript: {result.stderr}")
                
        except FileNotFoundError:
            raise EnvironmentError(
                "npm command not found. Please ensure Node.js and npm are installed and in your PATH.\n"
                "Download from: https://nodejs.org/\n"
                "After installation, restart your terminal/IDE and try again."
            )
    
    def run_dual_test(self, python_function: str, ts_function: str, test_data: Dict[str, Any]) -> tuple[Any, Any]:
        """
        Run a test against both Python and TypeScript implementations.
        
        Args:
            python_function: Name of the Python function to test
            ts_function: Name of the TypeScript function to test
            test_data: Dictionary containing 'input', 'expected', and optional 'mocks' and 'expected_error'
        
        Returns:
            Tuple of (python_result, typescript_result)
        """
        input_data = test_data["input"]
        mocks = test_data.get("mocks", {})
        expected_error = test_data.get("expected_error", False)
        
        py_result_holder = {}
        ts_result_holder = {}

        def run_python():
            py_result_holder["result"] = self._call_python_function_with_mocks(
                python_function, input_data, mocks.get("python", {}), expected_error
            )

        def run_typescript():
            ts_result_holder["result"] = self._call_typescript_function_with_mocks(
                ts_function, input_data, mocks.get("typescript", {}), expected_error
            )

        t_py = threading.Thread(target=run_python)
        t_ts = threading.Thread(target=run_typescript)
        t_py.start()
        t_ts.start()
        t_py.join()
        t_ts.join()

        py_result = py_result_holder["result"] if "result" in py_result_holder else None
        ts_result = ts_result_holder["result"] if "result" in ts_result_holder else None
        
        return py_result, ts_result
    
    def _call_python_function_with_mocks(self, function_name: str, input_data: Any, mocks: Dict[str, Any], expected_error: bool = False) -> Any:
        """Call a Python function with optional mocking."""
        try:
            # Apply mocks if provided
            mock_contexts = []
            for mock_target, mock_value in mocks.items():
                mock_contexts.append(patch(mock_target, return_value=mock_value))
            
            # Enter all mock contexts
            for mock_context in mock_contexts:
                mock_context.__enter__()
            
            try:
                # Call the appropriate function
                if function_name == "create_flexible_date":
                    result = create_flexible_date(input_data)
                elif function_name == "create_flexible_date_from_formal_date":
                    result = create_flexible_date_from_formal_date(input_data)
                elif function_name == "compare_two_dates":
                    fd1 = self._deserialize_flexible_date(input_data[0])
                    fd2 = self._deserialize_flexible_date(input_data[1])
                    result = compare_two_dates(fd1, fd2)
                elif function_name == "combine_flexible_dates":
                    dates = [self._deserialize_flexible_date(d) for d in input_data]
                    result = combine_flexible_dates(dates)
                elif function_name == "test_bool":
                    fd = self._deserialize_flexible_date(input_data)
                    result = bool(fd)
                elif function_name == "test_str":
                    fd = self._deserialize_flexible_date(input_data)
                    result = str(fd)
                elif function_name == "test_repr":
                    fd = self._deserialize_flexible_date(input_data)
                    result = repr(fd)
                elif function_name == "test_validator":
                    try:
                        fd = self._deserialize_flexible_date(input_data)
                        result = self._serialize_flexible_date(fd)
                    except (ValueError, PydanticValidationError) as e:
                        result = "ValueError"
                else:
                    raise ValueError(f"Unknown Python function: {function_name}")
                
                # Serialize the result for comparison
                if isinstance(result, FlexibleDate):
                    return self._serialize_flexible_date(result)
                else:
                    return result
                    
            finally:
                # Exit all mock contexts
                for mock_context in reversed(mock_contexts):
                    mock_context.__exit__(None, None, None)
                    
        except Exception as e:
            if expected_error:
                # Return a standardized error representation
                return {"error": True, "error_type": type(e).__name__, "error_message": str(e)}
            raise RuntimeError(f"Python function {function_name} failed: {str(e)}")
    
    def _call_typescript_function_with_mocks(self, function_name: str, input_data: Any, mocks: Dict[str, Any], expected_error: bool = False) -> Any:
        """Call a TypeScript function via subprocess with optional mocking."""
        try:
            # For combineFlexibleDates, input_data is a list of dates that should be passed as a single argument
            if function_name == "combineFlexibleDates":
                args = [input_data]
            else:
                args = [input_data] if not isinstance(input_data, list) else input_data
            
            request = {
                "method": function_name,
                "args": args,
                "mocks": mocks
            }
            
            # Call the TypeScript bridge
            result = subprocess.run(
                ["node", str(self.ts_bridge_path), json.dumps(request)],
                capture_output=True,
                text=True,
                cwd=str(self.root_dir)
            )

            if result.stderr:
                print("=== TypeScript Debug Output ===")
                print(result.stderr)
                print("================================")

            
            if result.returncode != 0:
                raise RuntimeError(f"TypeScript bridge failed: {result.stderr}")
            
            response = json.loads(result.stdout)
            
            if not response.get("success", False):
                if expected_error:
                    # Return a standardized error representation
                    return {"error": True, "error_type": "Error", "error_message": response.get('error', 'Unknown error')}
                raise RuntimeError(f"TypeScript function failed: {response.get('error', 'Unknown error')}")
            
            return response["result"]
            
        except json.JSONDecodeError as e:
            if expected_error:
                return {"error": True, "error_type": "JSONDecodeError", "error_message": str(e)}
            raise RuntimeError(f"Failed to parse TypeScript response: {str(e)}")
        except Exception as e:
            if expected_error:
                return {"error": True, "error_type": type(e).__name__, "error_message": str(e)}
            raise RuntimeError(f"TypeScript function {function_name} failed: {str(e)}")
    
    def _serialize_flexible_date(self, fd: FlexibleDate) -> Dict[str, Any]:
        """Convert a Python FlexibleDate to a serializable dictionary."""
        return {
            "likelyYear": fd.likely_year,
            "likelyMonth": fd.likely_month,
            "likelyDay": fd.likely_day
        }
    
    def _deserialize_flexible_date(self, data: Dict[str, Any]) -> FlexibleDate:
        """Convert a dictionary back to a Python FlexibleDate."""
        return FlexibleDate(
            likely_year=data.get("likelyYear"),
            likely_month=data.get("likelyMonth"),
            likely_day=data.get("likelyDay")
        )
    
    def compare_results(self, py_result: Any, ts_result: Any) -> bool:
        """
        Perform strict comparison between Python and TypeScript results.
        
        This method checks not only value equality but also:
        - Type consistency
        - Field presence and ordering (for dictionaries)
        - Null/None representation consistency
        - No extra metadata fields
        - Error state consistency (both errored or both succeeded)
        
        Args:
            py_result: Result from Python implementation
            ts_result: Result from TypeScript implementation
            
        Returns:
            bool: True if results are strictly identical, False otherwise
        """
        # Special handling for error results
        if isinstance(py_result, dict) and isinstance(ts_result, dict):
            # If both are error results, they match if both have error=True
            if py_result.get("error") is True and ts_result.get("error") is True:
                return True
        
        # Basic equality check
        if py_result != ts_result:
            return False
        
        # Type checking - must be exactly the same type
        if type(py_result) != type(ts_result):
            return False
        
        # For dictionaries, perform deep field-by-field comparison
        if isinstance(py_result, dict) and isinstance(ts_result, dict):
            # Check that both have exactly the same keys
            if set(py_result.keys()) != set(ts_result.keys()):
                return False
            
            # Check that each field has the same type
            for key in py_result.keys():
                py_value = py_result[key]
                ts_value = ts_result[key]
                
                # Recursive type checking for nested structures
                if type(py_value) != type(ts_value):
                    return False
                
                # For nested dictionaries, recurse
                if isinstance(py_value, dict) and isinstance(ts_value, dict):
                    if not self.compare_results(py_value, ts_value):
                        return False
        
        # For lists, check element types
        elif isinstance(py_result, list) and isinstance(ts_result, list):
            if len(py_result) != len(ts_result):
                return False
            
            for py_item, ts_item in zip(py_result, ts_result):
                if not self.compare_results(py_item, ts_item):
                    return False
        
        return True
    
    def assert_strict_parity(self, py_result: Any, ts_result: Any, context: str = ""):
        """
        Assert strict parity between Python and TypeScript results with detailed error reporting.
        
        Args:
            py_result: Result from Python implementation
            ts_result: Result from TypeScript implementation  
            context: Additional context for error messages
            
        Raises:
            AssertionError: If results are not strictly identical, with detailed explanation
        """
        if not self.compare_results(py_result, ts_result):
            error_details = []
            
            # Basic equality
            if py_result != ts_result:
                error_details.append(f"Value mismatch: Python={py_result}, TypeScript={ts_result}")
            
            # Type checking
            if type(py_result) != type(ts_result):
                error_details.append(f"Type mismatch: Python={type(py_result).__name__}, TypeScript={type(ts_result).__name__}")
                error_details.append(f"Python value: {py_result}, TypeScript value: {ts_result}")
            
            # Dictionary field analysis
            if isinstance(py_result, dict) and isinstance(ts_result, dict):
                py_keys = set(py_result.keys())
                ts_keys = set(ts_result.keys())
                
                if py_keys != ts_keys:
                    missing_in_ts = py_keys - ts_keys
                    missing_in_py = ts_keys - py_keys
                    if missing_in_ts:
                        error_details.append(f"Fields missing in TypeScript: {missing_in_ts}")
                    if missing_in_py:
                        error_details.append(f"Fields missing in Python: {missing_in_py}")
                
                # Field type mismatches
                for key in py_keys & ts_keys:
                    if type(py_result[key]) != type(ts_result[key]):
                        error_details.append(f"Field '{key}' type mismatch: Python={type(py_result[key]).__name__}, TypeScript={type(ts_result[key]).__name__}")
            
            context_str = f" ({context})" if context else ""
            raise AssertionError(f"Implementation parity check failed{context_str}:\n" + "\n".join(f"  - {detail}" for detail in error_details))