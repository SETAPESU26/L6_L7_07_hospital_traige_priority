"""No-crash properties: unexpected exceptions must fail the test."""
import pytest
from hypothesis import given, settings, strategies as st
from processor import parse_vitals_summary, compute_patient_bmi, assign_ward_bed


@settings(max_examples=300, derandomize=True)
@given(st.text() | st.none())
def test_parse_vitals_summary_no_crash(s):
    try:
        result = parse_vitals_summary(s)
    except Exception as exc:
        pytest.fail(f"parse_vitals_summary crashed for {s!r}: {exc!r}")
    assert isinstance(result, str)


@settings(max_examples=300, derandomize=True)
@given(st.text() | st.none())
def test_compute_patient_bmi_safe(s):
    try:
        result = compute_patient_bmi(s)
    except Exception as exc:
        pytest.fail(f"compute_patient_bmi crashed for {s!r}: {exc!r}")
    assert result is None or isinstance(result, float)


@settings(max_examples=300, derandomize=True)
@given(st.text() | st.none())
def test_assign_ward_bed_safe(s):
    try:
        result = assign_ward_bed(s)
    except Exception as exc:
        pytest.fail(f"assign_ward_bed crashed for {s!r}: {exc!r}")
    assert isinstance(result, str)
