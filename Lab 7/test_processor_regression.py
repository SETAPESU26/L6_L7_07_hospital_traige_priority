"""Structured fuzzing and regression tests supplement arbitrary Unicode."""
import math
import subprocess
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st
from processor import (
    INVALID_ALLOCATION, INVALID_VITALS, assign_ward_bed,
    compute_patient_bmi, parse_vitals_summary,
)


@pytest.mark.parametrize('value', [None, '', ' ', 42, [], {}, True])
def test_wrong_types_and_empty_inputs(value):
    assert parse_vitals_summary(value) == INVALID_VITALS
    assert compute_patient_bmi(value) is None
    assert assign_ward_bed(value) == INVALID_ALLOCATION


@pytest.mark.parametrize('value', ['75', '75,98', '75,98,37,1', ',,',
    'x,98,37', 'nan,98,37', '75,inf,37', '75,98,-inf',
    '0,98,37', '75,0,37', '75,101,37', '75,98,0', '1e999,98,37', '9'*1001])
def test_invalid_vitals(value):
    assert parse_vitals_summary(value) == INVALID_VITALS


@pytest.mark.parametrize('value,label', [
    ('120,90,39', 'STABLE'), ('121,98,37', 'CRITICAL'),
    ('75,89,37', 'CRITICAL'), ('75,98,39.1', 'CRITICAL'),
])
def test_critical_boundaries(value, label):
    assert parse_vitals_summary(value).endswith(label)


@pytest.mark.parametrize('value', ['70', '70/', '/1.75', '70/1/2', 'x/y',
    '70/0', '-70/1.75', '70/-1', 'nan/1', '70/inf', '1e999/1',
    '70/1e-300', '70/1e300', '1e-300/1e100', '1e300/1e-100', '9'*1001])
def test_invalid_bmi(value):
    assert compute_patient_bmi(value) is None


@pytest.mark.parametrize('value', ['ICU', 'ICU-', '-1', 'ICU-0', 'ICU--1',
    'ICU-1-2', 'UNKNOWN-1', 'GEN-1.5', 'ER-+1', 'ICU-\u0661', 'ICU-'+'9'*1000])
def test_invalid_allocations(value):
    assert assign_ward_bed(value) == INVALID_ALLOCATION


def test_valid_examples_and_whitespace():
    assert parse_vitals_summary(' 75 , 98 , 37 ') == 'Vitals: HR=75.0, SpO2=98.0% - STABLE'
    assert compute_patient_bmi(' 70 / 1.75 ') == 22.86
    assert assign_ward_bed(' icu - 05 ') == 'Intensive Care Unit Bed #5'


@settings(max_examples=200, derandomize=True)
@given(st.integers(1, 300), st.integers(1, 100), st.integers(1, 45))
def test_structured_vitals(hr, spo2, temp):
    label = 'CRITICAL' if hr > 120 or spo2 < 90 or temp > 39 else 'STABLE'
    assert parse_vitals_summary(f'{hr},{spo2},{temp}') == (
        f'Vitals: HR={float(hr)}, SpO2={float(spo2)}% - {label}')


@settings(max_examples=200, derandomize=True)
@given(st.integers(1, 500), st.integers(50, 250))
def test_structured_bmi(weight, height_cm):
    height = height_cm / 100
    assert compute_patient_bmi(f'{weight}/{height}') == round(weight / height ** 2, 2)


@settings(max_examples=200, derandomize=True)
@given(st.sampled_from([('ER', 'Emergency Room'), ('ICU', 'Intensive Care Unit'),
                       ('GEN', 'General Ward'), ('PED', 'Pediatrics')]),
       st.integers(1, 1000000))
def test_structured_allocations(ward, bed):
    assert assign_ward_bed(f'{ward[0].lower()}-{bed:05d}') == f'{ward[1]} Bed #{bed}'


@settings(max_examples=200, derandomize=True)
@given(st.floats(allow_nan=True, allow_infinity=True),
       st.floats(allow_nan=True, allow_infinity=True))
def test_extreme_bmi_is_safe(weight, height):
    result = compute_patient_bmi(f'{weight}/{height}')
    assert result is None or (math.isfinite(result) and result > 0)


def test_cli_handles_eof():
    result = subprocess.run([sys.executable, str(Path(__file__).with_name('processor.py'))],
                            input='', capture_output=True, text=True)
    assert result.returncode == 0
    assert 'Input cancelled.' in result.stdout
