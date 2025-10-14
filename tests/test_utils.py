import json
import subprocess
import sys
import os
import threading
from pathlib import Path
from typing import Any, Dict, Optional
from unittest.mock import patch, MagicMock

# Add the FlexibleDate module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'FlexibleDate'))
from FlexibleDate import FlexibleDate, create_flexible_date, create_flexible_date_from_formal_date, compare_two_dates, combine_flexible_dates


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
            test_data: Dictionary containing 'input', 'expected', and optional 'mocks'
        
        Returns:
            Tuple of (python_result, typescript_result)
        """
        input_data = test_data["input"]
        mocks = test_data.get("mocks", {})
        
        # Run Python function with mocking
        py_result = self._call_python_function_with_mocks(python_function, input_data, mocks.get("python", {}))
        
        # Run TypeScript function with mocking
        ts_result = self._call_typescript_function_with_mocks(ts_function, input_data, mocks.get("typescript", {}))
        
        return py_result, ts_result
    
    def _call_python_function_with_mocks(self, function_name: str, input_data: Any, mocks: Dict[str, Any]) -> Any:
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
            raise RuntimeError(f"Python function {function_name} failed: {str(e)}")
    
    def _call_typescript_function_with_mocks(self, function_name: str, input_data: Any, mocks: Dict[str, Any]) -> Any:
        """Call a TypeScript function via subprocess with optional mocking."""
        try:
            request = {
                "method": function_name,
                "args": [input_data] if not isinstance(input_data, list) else input_data,
                "mocks": mocks
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
                raise RuntimeError(f"TypeScript function failed: {response.get('error', 'Unknown error')}")
            
            return response["result"]
            
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse TypeScript response: {str(e)}")
        except Exception as e:
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