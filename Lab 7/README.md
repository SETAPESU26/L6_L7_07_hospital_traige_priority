# Lab 7 - Fuzz Testing with Hypothesis

- `processor.py`: input-safe implementation with the original valid output format.
- `test_processor.py`: three completed text/None no-crash properties (300 examples each).
- `test_processor_regression.py`: regression tests and four structured properties (200 each).
- `baseline/`: original implementation and the three properties, intentionally failing.
- `evidence/`: original failures, fixed outputs, screenshots, and passing test statistics.
- `../reports/Lab7_Fuzz_Testing_Report.pdf`: screenshot report and bug analysis.

All 61 Lab 7 tests pass, including 1,700 generated examples. See the root README
for the input contract, commands, and baseline reproduction instructions.
