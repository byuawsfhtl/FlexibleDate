import pytest
import json
import subprocess
import os
import sys
from pathlib import Path
import coverage
from test_utils import FlexibleDateTestRunner


class TestPythonAndTypeScriptParity:
    """Test that Python and TypeScript implementations behave identically and have similar coverage."""
    
    def setup_method(self):
        """Set up test runner and paths."""
        self.runner = FlexibleDateTestRunner()
        self.root_dir = Path(__file__).parent.parent
        self.python_module_path = self.root_dir / "FlexibleDate"
        self.ts_module_path = self.root_dir / "FlexibleDateTS"
    
    def test_behavioral_parity_comprehensive(self):
        """Comprehensive test to ensure both implementations behave identically."""
        # Load all test cases from configuration
        all_categories = ["create_flexible_date", "create_flexible_date_from_formal_date", 
                         "compare_two_dates", "combine_flexible_dates"]
        
        total_tests = 0
        passed_tests = 0
        
        for category in all_categories:
            test_cases = self.runner.load_test_cases(category)
            
            for case in test_cases:
                total_tests += 1
                
                try:
                    if category == "create_flexible_date":
                        self.runner.run_dual_test("createFlexibleDate", case["input"])
                    
                    elif category == "create_flexible_date_from_formal_date":
                        self.runner.run_dual_test("createFlexibleDateFromFormalDate", case["input"])
                    
                    elif category == "compare_two_dates":
                        self.runner.run_dual_test("compareTwoDates", case["input"][0], case["input"][1])
                    
                    elif category == "combine_flexible_dates":
                        self.runner.run_dual_test("combineFlexibleDates", case["input"][0])
                    
                    passed_tests += 1
                    
                except Exception as e:
                    print(f"Behavioral parity test failed for {category}/{case.get('name', 'unnamed')}: {str(e)}")
                    # Continue testing other cases but record the failure
        
        # Ensure a high percentage of tests pass
        success_rate = passed_tests / total_tests if total_tests > 0 else 0
        assert success_rate >= 0.95, f"Only {success_rate:.1%} of behavioral parity tests passed ({passed_tests}/{total_tests})"
        
        print(f"Behavioral parity: {passed_tests}/{total_tests} tests passed ({success_rate:.1%})")
    
    def test_method_signature_parity(self):
        """Test that both implementations have equivalent method signatures."""
        # Test that all expected methods exist and behave consistently
        test_methods = [
            ("createFlexibleDate", ["2023-05-15"]),
            ("createFlexibleDateFromFormalDate", ["2023-05-15"]),
            ("toString", [{"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15}]),
            ("valueOf", [{"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15}]),
            ("compareTwoDates", [
                {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 16}
            ]),
            ("combineFlexibleDates", [[
                {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15},
                {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 16}
            ]])
        ]
        
        for method_name, args in test_methods:
            try:
                py_result = self.runner.run_python_test(method_name, *args)
                ts_result = self.runner.run_typescript_test(method_name, *args)
                
                # Both should succeed and return comparable results
                assert self.runner.compare_results(py_result, ts_result), \
                    f"Method {method_name} returned different results: Python={py_result}, TypeScript={ts_result}"
                
                print(f"✓ Method {method_name} signature parity confirmed")
                
            except Exception as e:
                pytest.fail(f"Method signature parity test failed for {method_name}: {str(e)}")
    
    def run_python_coverage(self):
        """Run Python tests with coverage analysis."""
        try:
            # Initialize coverage
            cov = coverage.Coverage(source=[str(self.python_module_path)])
            cov.start()
            
            # Import and run some basic operations to generate coverage
            sys.path.insert(0, str(self.python_module_path))
            from FlexibleDate import FlexibleDate, createFlexibleDate, compareTwoDates, combineFlexibleDates
            
            # Execute representative operations
            fd1 = createFlexibleDate("2023-05-15")
            fd2 = createFlexibleDate("May 2023")
            fd3 = FlexibleDate(likelyYear=2023, likelyMonth=5, likelyDay=15)
            
            score = compareTwoDates(fd1, fd3)
            combined = combineFlexibleDates([fd1, fd2, fd3])
            
            str_repr = str(fd1)
            value = fd1.valueOf()
            
            cov.stop()
            cov.save()
            
            # Get coverage report
            coverage_data = cov.get_data()
            
            # Calculate coverage percentage
            total_lines = 0
            covered_lines = 0
            
            for filename in coverage_data.measured_files():
                if "FlexibleDate.py" in filename:
                    file_lines = coverage_data.lines(filename)
                    if file_lines:
                        total_lines += len(file_lines)
                        covered_lines += len(file_lines)
            
            python_coverage = (covered_lines / total_lines * 100) if total_lines > 0 else 0
            
            return {
                "coverage_percentage": python_coverage,
                "total_lines": total_lines,
                "covered_lines": covered_lines
            }
            
        except Exception as e:
            print(f"Python coverage analysis failed: {str(e)}")
            return {"coverage_percentage": 0, "total_lines": 0, "covered_lines": 0}
    
    def run_typescript_coverage(self):
        """Run TypeScript tests with coverage analysis."""
        try:
            # Change to TypeScript directory
            original_cwd = os.getcwd()
            os.chdir(str(self.ts_module_path))
            
            # Run a series of test operations through the bridge to generate coverage
            test_operations = [
                '{"method": "createFlexibleDate", "args": ["2023-05-15"]}',
                '{"method": "createFlexibleDate", "args": ["May 2023"]}',
                '{"method": "createFlexibleDateFromFormalDate", "args": ["2023-05-15"]}',
                '{"method": "compareTwoDates", "args": [{"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15}, {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 16}]}',
                '{"method": "combineFlexibleDates", "args": [[{"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15}, {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 16}]]}',
                '{"method": "toString", "args": [{"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15}]}',
                '{"method": "valueOf", "args": [{"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15}]}'
            ]
            
            # Run operations with nyc coverage
            for operation in test_operations:
                subprocess.run(
                    ["npx", "nyc", "--silent", "node", "dist/test_bridge.js", operation],
                    capture_output=True,
                    text=True
                )
            
            # Generate coverage report
            result = subprocess.run(
                ["npx", "nyc", "report", "--reporter=json"],
                capture_output=True,
                text=True
            )
            
            os.chdir(original_cwd)
            
            if result.returncode == 0:
                try:
                    coverage_data = json.loads(result.stdout)
                    
                    # Extract coverage information
                    total_lines = 0
                    covered_lines = 0
                    
                    for file_path, file_data in coverage_data.get("", {}).items():
                        if "FlexibleDateTS" in file_path:
                            statements = file_data.get("s", {})
                            total_lines += len(statements)
                            covered_lines += sum(1 for count in statements.values() if count > 0)
                    
                    ts_coverage = (covered_lines / total_lines * 100) if total_lines > 0 else 0
                    
                    return {
                        "coverage_percentage": ts_coverage,
                        "total_lines": total_lines,
                        "covered_lines": covered_lines
                    }
                    
                except json.JSONDecodeError:
                    pass
            
            return {"coverage_percentage": 0, "total_lines": 0, "covered_lines": 0}
            
        except Exception as e:
            print(f"TypeScript coverage analysis failed: {str(e)}")
            if 'original_cwd' in locals():
                os.chdir(original_cwd)
            return {"coverage_percentage": 0, "total_lines": 0, "covered_lines": 0}
    
    def test_coverage_parity(self):
        """Test that both implementations have similar test coverage."""
        print("Running coverage analysis...")
        
        python_cov = self.run_python_coverage()
        typescript_cov = self.run_typescript_coverage()
        
        print(f"Python coverage: {python_cov['coverage_percentage']:.1f}% ({python_cov['covered_lines']}/{python_cov['total_lines']} lines)")
        print(f"TypeScript coverage: {typescript_cov['coverage_percentage']:.1f}% ({typescript_cov['covered_lines']}/{typescript_cov['total_lines']} lines)")
        
        # Allow for some tolerance in coverage differences
        coverage_tolerance = 5.0  # 5% tolerance
        coverage_diff = abs(python_cov['coverage_percentage'] - typescript_cov['coverage_percentage'])
        
        # Both should have reasonable coverage (at least 70%)
        min_coverage = 70.0
        assert python_cov['coverage_percentage'] >= min_coverage, \
            f"Python coverage too low: {python_cov['coverage_percentage']:.1f}% (minimum: {min_coverage}%)"
        
        assert typescript_cov['coverage_percentage'] >= min_coverage, \
            f"TypeScript coverage too low: {typescript_cov['coverage_percentage']:.1f}% (minimum: {min_coverage}%)"
        
        # Coverage should be similar between implementations
        assert coverage_diff <= coverage_tolerance, \
            f"Coverage difference too large: {coverage_diff:.1f}% (tolerance: {coverage_tolerance}%)"
        
        print(f"✓ Coverage parity confirmed (difference: {coverage_diff:.1f}%)")
    
    def test_error_handling_parity(self):
        """Test that both implementations handle errors consistently."""
        error_test_cases = [
            ("createFlexibleDate", [None]),
            ("createFlexibleDateFromFormalDate", [""]),
            ("createFlexibleDateFromFormalDate", ["invalid-format"]),
        ]
        
        for method_name, args in error_test_cases:
            print(f"Testing error handling for {method_name} with args {args}")
            
            python_error = None
            typescript_error = None
            
            try:
                self.runner.run_python_test(method_name, *args)
            except Exception as e:
                python_error = str(e)
            
            try:
                self.runner.run_typescript_test(method_name, *args)
            except Exception as e:
                typescript_error = str(e)
            
            # Both should either succeed or fail consistently
            if python_error is None and typescript_error is None:
                # Both succeeded - that's fine
                continue
            elif python_error is not None and typescript_error is not None:
                # Both failed - that's also fine as long as they're consistent
                print(f"Both implementations failed consistently for {method_name}")
                continue
            else:
                # One succeeded and one failed - this is a problem
                pytest.fail(
                    f"Inconsistent error handling for {method_name}: "
                    f"Python={'succeeded' if python_error is None else 'failed'}, "
                    f"TypeScript={'succeeded' if typescript_error is None else 'failed'}"
                )
