# FlexibleDate Dual-Language Testing Framework

This testing framework ensures that both Python and TypeScript implementations of FlexibleDate behave identically and maintain coverage parity.

## Architecture

The framework uses a **subprocess-based approach** where Python tests call the TypeScript implementation via a Node.js bridge, comparing results to ensure consistency.

### Core Components

1. **`test_utils.py`** - Cross-language test utilities and runner
2. **`test_config.json`** - Centralized test case definitions
3. **`FlexibleDateTS/test_bridge.ts`** - TypeScript bridge for cross-language testing
4. **Individual test files** - Test both implementations simultaneously
5. **`test_python_and_ts_work_the_same.py`** - Coverage and behavioral parity tests

## Running Tests

### Quick Start
```bash
# Run all tests with coverage
python run_tests.py

# Run tests without coverage
python run_tests.py --no-coverage

# Run verbose tests
python run_tests.py --verbose
```

### Specific Test Categories
```bash
# Test date creation
python run_tests.py --category create

# Test EDTF parsing
python run_tests.py --category formal

# Test date comparison
python run_tests.py --category compare

# Test date combination
python run_tests.py --category combine

# Test implementation parity
python run_tests.py --category parity
```

### Setup Only
```bash
# Just compile TypeScript and verify environment
python run_tests.py --setup-only
```

## Test Structure

### Individual Test Files
Each test file tests both implementations:

- **`test_create_flexible_date.py`** - Date creation from strings
- **`test_create_flexible_date_from_formal_date.py`** - EDTF format parsing
- **`test_compare_two_dates.py`** - Date comparison functionality
- **`test_combine_flexible_dates.py`** - Date combination logic

### Parity Tests
**`test_python_and_ts_work_the_same.py`** ensures:
- Behavioral consistency between implementations
- Similar test coverage percentages
- Consistent error handling
- Method signature compatibility

## Adding New Tests

### 1. Add Test Cases to Configuration
Edit `test_config.json`:
```json
{
  "your_category": {
    "test_group": [
      {
        "name": "descriptive_name",
        "input": "test_input",
        "expected": {"expected": "result"}
      }
    ]
  }
}
```

### 2. Update Test Files
Use the `FlexibleDateTestRunner`:
```python
def test_your_functionality(self):
    test_cases = self.runner.load_test_cases("your_category", "test_group")
    
    for case in test_cases:
        self.runner.run_dual_test(
            "methodName",
            case["input"],
            expected=case["expected"]
        )
```

### 3. Update TypeScript Bridge (if needed)
Add new method handling in `FlexibleDateTS/test_bridge.ts`:
```typescript
case 'newMethod':
    // Handle new method
    return { success: true, result: ... };
```

## Coverage Requirements

- **Minimum Coverage**: 70% for both implementations
- **Coverage Tolerance**: 5% difference between Python and TypeScript
- **Behavioral Parity**: 95% of tests must pass for both implementations

## Dependencies

### Python
- `pytest` - Test framework
- `coverage` - Coverage analysis
- `json` - Test configuration parsing

### TypeScript
- `nyc` - Coverage analysis
- `ts-node` - TypeScript execution
- `typescript` - TypeScript compiler

## Troubleshooting

### TypeScript Bridge Not Found
```bash
cd FlexibleDateTS
npm run build
```

### Coverage Analysis Fails
Ensure all dependencies are installed:
```bash
pip install coverage pytest
cd FlexibleDateTS && npm install
```

### Tests Fail Due to Implementation Differences
1. Check the specific test output
2. Verify both implementations handle the case correctly
3. Update test expectations if needed
4. Ensure TypeScript bridge correctly serializes/deserializes data

## Benefits

1. **Single Source of Truth**: Test cases defined once in JSON
2. **Automatic Synchronization**: Tests fail if implementations diverge  
3. **Coverage Parity**: Ensures both versions are equally well-tested
4. **Maintainable**: Standard subprocess approach, familiar to developers
5. **Extensible**: Easy to add new test cases or methods
