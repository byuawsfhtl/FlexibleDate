# Self-Contained Dual-Language Testing Framework

This testing framework automatically tests both Python and TypeScript implementations of FlexibleDate to ensure they behave identically.

## Key Features

- **Self-contained setup** - Automatically handles Node.js environment and TypeScript compilation
- **Dual-language testing** - Every test runs against both implementations simultaneously
- **Coverage-aware** - Python code execution is measured by coverage tools
- **Strict parity enforcement** - Tests fail if implementations return different results, types, or structures
- **Enhanced comparison** - Catches subtle differences like type mismatches and extra fields
- **Mocking support** - Can mock dependencies in both Python and TypeScript environments

## Usage

Simply run pytest as normal:

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_create_flexible_date.py -v

# Run with coverage (works with TestCoverageAction)
pytest tests/ --cov=FlexibleDate --cov-report=term-missing
```

## Test Structure

Each test uses the `FlexibleDateTestRunner` with this pattern:

```python
from test_utils import FlexibleDateTestRunner

test_runner = FlexibleDateTestRunner()

def test_example():
    test_data = {
        "input": "2023-05-15",
        "expected": {"likelyYear": 2023, "likelyMonth": 5, "likelyDay": 15},
        "mocks": {}  # Optional mocking configuration
    }
    
    py_result, ts_result = test_runner.run_dual_test(
        "create_flexible_date",    # Python function name
        "createFlexibleDate",      # TypeScript function name
        test_data
    )
    
    # Standard pytest assertions
    assert py_result == test_data["expected"]
    assert ts_result == test_data["expected"]
    
    # Strict parity check - catches type mismatches and structural differences
    test_runner.assert_strict_parity(py_result, ts_result, "test context")
```

## Mocking Support

The framework supports mocking dependencies in both languages:

```python
test_data = {
    "input": "test input",
    "expected": {"result": "expected"},
    "mocks": {
        "python": {
            "module.function": "mock_return_value"
        },
        "typescript": {
            "functionName": "mock_return_value"
        }
    }
}
```

## Environment Setup

The test runner automatically:

1. **Checks for Node.js** availability
2. **Verifies TypeScript compilation** status
3. **Compiles TypeScript if needed** (only when necessary)
4. **Sets up the testing environment** once per test session

## CI Integration

This framework works seamlessly with TestCoverageAction:

- Python code execution is measured by coverage tools
- TypeScript execution happens via subprocess (not measured, but that's expected)
- Standard pytest workflow is preserved
- No special CI configuration needed beyond ensuring Node.js is available

## Benefits

- ✅ **Zero configuration** - Just run pytest
- ✅ **Automatic parity checking** - Implementations can't diverge
- ✅ **Proper coverage measurement** - Python code is measured correctly
- ✅ **Self-contained** - No external setup scripts needed
- ✅ **Developer friendly** - Standard pytest workflow
- ✅ **CI compatible** - Works with existing TestCoverageAction
