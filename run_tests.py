#!/usr/bin/env python3
"""
Unified test runner for FlexibleDate dual-language testing framework.

This script runs all tests for both Python and TypeScript implementations,
ensuring behavioral consistency and coverage parity.
"""

import sys
import subprocess
import os
from pathlib import Path
import argparse


def run_command(command, cwd=None, description=""):
    """Run a command and return the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=False,  # Show output in real-time
            text=True
        )
        
        if result.returncode != 0:
            print(f"FAILED: {description} failed with exit code {result.returncode}")
            return False
        else:
            print(f"SUCCESS: {description} completed successfully")
            return True
            
    except Exception as e:
        print(f"ERROR: {description} failed with exception: {str(e)}")
        return False


def setup_environment():
    """Set up the testing environment."""
    root_dir = Path(__file__).parent
    ts_dir = root_dir / "FlexibleDateTS"
    
    print("Setting up testing environment...")
    
    # Ensure TypeScript is compiled
    if not run_command(
        ["npm", "run", "build"],
        cwd=str(ts_dir),
        description="Compiling TypeScript code"
    ):
        return False
    
    # Verify test bridge exists
    bridge_path = ts_dir / "dist" / "test_bridge.js"
    if not bridge_path.exists():
        print(f"ERROR: TypeScript test bridge not found at {bridge_path}")
        return False
    
    print("SUCCESS: Environment setup completed")
    return True


def run_python_tests(coverage=True, verbose=False):
    """Run Python tests with optional coverage."""
    root_dir = Path(__file__).parent
    
    # Prepare pytest command
    pytest_cmd = ["python", "-m", "pytest"]
    
    if verbose:
        pytest_cmd.append("-v")
    
    if coverage:
        pytest_cmd.extend([
            "--cov=FlexibleDate",
            "--cov-report=term-missing",
            "--cov-report=json:coverage_python.json"
        ])
    
    pytest_cmd.append("tests/")
    
    return run_command(
        pytest_cmd,
        cwd=str(root_dir),
        description="Running Python tests with dual-language framework"
    )


def run_typescript_coverage():
    """Run TypeScript coverage analysis."""
    root_dir = Path(__file__).parent
    ts_dir = root_dir / "FlexibleDateTS"
    
    # Run some test operations to generate coverage
    test_operations = [
        '{"method": "createFlexibleDate", "args": ["2023-05-15"]}',
        '{"method": "createFlexibleDateFromFormalDate", "args": ["2023-05-15"]}',
        '{"method": "compareTwoDates", "args": [{"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15}, {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 16}]}',
        '{"method": "combineFlexibleDates", "args": [[{"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15}]]}',
        '{"method": "toString", "args": [{"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15}]}',
        '{"method": "valueOf", "args": [{"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15}]}'
    ]
    
    print("\nRunning TypeScript operations for coverage analysis...")
    
    for i, operation in enumerate(test_operations):
        success = run_command(
            ["npx", "nyc", "--silent", "node", "dist/test_bridge.js", operation],
            cwd=str(ts_dir),
            description=f"TypeScript operation {i+1}/{len(test_operations)}"
        )
        if not success:
            return False
    
    # Generate coverage report
    return run_command(
        ["npx", "nyc", "report", "--reporter=text", "--reporter=json"],
        cwd=str(ts_dir),
        description="Generating TypeScript coverage report"
    )


def run_specific_test_category(category, verbose=False):
    """Run tests for a specific category."""
    root_dir = Path(__file__).parent
    
    test_files = {
        "create": "tests/test_create_flexible_date.py",
        "formal": "tests/test_create_flexible_date_from_formal_date.py",
        "compare": "tests/test_compare_two_dates.py",
        "combine": "tests/test_combine_flexible_dates.py",
        "parity": "tests/test_python_and_ts_work_the_same.py"
    }
    
    if category not in test_files:
        print(f"ERROR: Unknown test category: {category}")
        print(f"Available categories: {', '.join(test_files.keys())}")
        return False
    
    pytest_cmd = ["python", "-m", "pytest"]
    if verbose:
        pytest_cmd.append("-v")
    pytest_cmd.append(test_files[category])
    
    return run_command(
        pytest_cmd,
        cwd=str(root_dir),
        description=f"Running {category} tests"
    )


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(
        description="Unified test runner for FlexibleDate dual-language testing"
    )
    parser.add_argument(
        "--category",
        choices=["create", "formal", "compare", "combine", "parity"],
        help="Run tests for a specific category only"
    )
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Skip coverage analysis"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose test output"
    )
    parser.add_argument(
        "--setup-only",
        action="store_true",
        help="Only set up the environment, don't run tests"
    )
    
    args = parser.parse_args()
    
    print("FlexibleDate Dual-Language Test Runner")
    print("=" * 60)
    
    # Set up environment
    if not setup_environment():
        print("\nEnvironment setup failed")
        sys.exit(1)
    
    if args.setup_only:
        print("\nEnvironment setup completed. Exiting as requested.")
        sys.exit(0)
    
    success = True
    
    # Run specific category or all tests
    if args.category:
        success = run_specific_test_category(args.category, args.verbose)
    else:
        # Run all Python tests
        success = run_python_tests(coverage=not args.no_coverage, verbose=args.verbose)
        
        # Run TypeScript coverage if requested
        if success and not args.no_coverage:
            success = run_typescript_coverage()
    
    # Final summary
    print("\n" + "=" * 60)
    if success:
        print("SUCCESS: All tests completed successfully!")
        print("SUCCESS: Both Python and TypeScript implementations are working correctly")
        if not args.no_coverage:
            print("INFO: Coverage analysis completed")
    else:
        print("FAILED: Some tests failed")
        print("INFO: Check the output above for details")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
