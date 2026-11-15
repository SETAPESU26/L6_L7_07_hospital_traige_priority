# Hospital Triage Priority - Labs 6 and 7

Completed from the starter at commit `445d681ad139a69d90875adfb053916050c37b8f`.
This is an educational testing exercise; its thresholds are assignment rules.

## Setup and verification

Use Python 3.12 (the version used for this submission).

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q -W error
```

Verified result: **93 passed**, with no warnings. The GitHub Actions workflow
runs the tests and enforces both the combined coverage score and the separate
Lab 6 branch percentage at 90% or higher.

## Deliverables

| Lab | Files | Verified result |
| --- | --- | --- |
| 6 | `Lab 6/CodeCoverageTest_hospital_triage_priority.py` | 10 tests; 45/45 statements (100%) |
| 6 | `Lab 6/BranchCoverageTest_hospital_triage_priority.py` plus line suite | 31 tests; 32/32 branches (100%) |
| 7 | `Lab 7/processor.py`, `Lab 7/test_processor.py`, `Lab 7/test_processor_regression.py` | 61 tests; 1,700 generated examples |

PDF reports are in `reports/`. Each lab's `evidence/` folder contains screenshots
and the underlying verbatim logs; Lab 6 also contains machine-readable coverage
JSON. Screenshots are browser captures of the recorded terminal transcripts,
not native console-window captures. No results were manually invented.

Lab 6's application and its original starter test are unchanged. Its separate
test files and evidence are recorded in separate code-coverage and
branch-coverage commits as required by the handout.

Lab 7's `baseline/processor.py` preserves the original application. The same
three no-crash properties were first run against it, producing 3 failed tests
and 11 minimized failure variants. The baseline is intentionally broken and
excluded from the normal suite. Full traceback evidence is retained.

## Lab 6 commands

Run inside `Lab 6`:

```sh
python -m coverage run --source=hospital_triage_priority -m pytest CodeCoverageTest_hospital_triage_priority.py -q
python -m coverage report -m --fail-under=90
python -m coverage run --branch --source=hospital_triage_priority -m pytest CodeCoverageTest_hospital_triage_priority.py BranchCoverageTest_hospital_triage_priority.py -q
python -m coverage report -m --fail-under=90
python -m coverage json -o evidence/branch_coverage.json
python -m coverage html
```

The starter test measured 21/45 statements (46.67%). With branch measurement,
the terminal's initial 43% is the combined statement-and-branch score, not a
standalone branch percentage. Final JSON confirms no missing lines or branches.

Tests cover invalid arguments, accepting/closed/empty wards, default values,
normal/urgent/unconscious patients, both sides of vital thresholds, the 4/5
alert boundary, outpatient reset and break, ICU standby, and oxygen streak
reset/isolation across manifolds. Coverage is not proof of clinical correctness
or exhaustive path coverage.

## Lab 7 input contract

| Function | Valid input | Invalid result |
| --- | --- | --- |
| `parse_vitals_summary` | Three finite numbers: HR > 0, 0 < SpO2 <= 100, temperature > 0 | `Invalid vitals summary` |
| `compute_patient_bmi` | Positive finite weight in kg / height in metres; finite, positive rounded result | `None` |
| `assign_ward_bed` | ER, ICU, GEN, or PED; hyphen; positive ASCII integer bed | `Invalid ward allocation` |

Whitespace and ward-name case are normalized. Inputs longer than 1,000
characters are rejected. The valid starter output format and critical thresholds
(HR > 120, SpO2 < 90, temperature > 39) are preserved. BMI arithmetic guards
division by zero, overflow, underflow, NaN, and infinity. The CLI reports invalid
data and exits cleanly if input is cancelled or ends early.

Run inside `Lab 7`:

```sh
python processor.py
python -m pytest test_processor.py test_processor_regression.py -q --hypothesis-show-statistics
```

To reproduce the original failures, run separately inside `Lab 7/baseline`:

```sh
python -m pytest test_processor.py -q --tb=short
```

That command is expected to fail. The three main properties use 300 examples
each; four structured properties use 200 each. Fixed deterministic settings make
the runs repeatable with the pinned versions, but do not prove safety for every
possible input. Explicit regression tests assert both correct valid outputs and
safe invalid results; the no-crash tests fail on exceptions rather than hiding them.
