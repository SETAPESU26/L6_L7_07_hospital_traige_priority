"""Branch and boundary tests complementing the line coverage suite."""
import pytest
from hospital_triage_priority import monitor_oxygen_manifolds, process_triage_wards


@pytest.mark.parametrize("spo2,hr,expected", [
    (90, 120, 10), (89, 120, 60), (90, 121, 60),
    (0, 75, 0), (95, 0, 0), (-1, 75, 0), (95, -1, 0),
])
def test_vital_boundaries(spo2, hr, expected):
    result = process_triage_wards([
        {"is_accepting": True, "patients": [{"spo2": spo2, "hr": hr}]}], 10)
    assert result == {"acuity_score": expected,
                      "status": "TRIAGE_STABLE" if expected else "NO_URGENT_CASES"}


@pytest.mark.parametrize("count,status", [(4, "NO_URGENT_CASES"), (5, "WARD_ALERT")])
def test_alert_threshold(count, status):
    result = process_triage_wards([
        {"is_accepting": True, "patients": [{"hr": 0}] * count}], 10)
    assert result == {"acuity_score": 0, "status": status}


def test_unconscious_patients_also_count_toward_alert():
    result = process_triage_wards([
        {"is_accepting": True, "patients": [{"unconscious": True}] * 5}], 10)
    assert result == {"acuity_score": 500, "status": "WARD_ALERT"}


def test_outpatient_break_preserves_outer_loop_and_standby():
    wards = [
        {"is_accepting": True, "patients": [{}]},
        {"is_accepting": True, "tier": "outpatient", "icu_standby": True,
         "patients": [{"unconscious": True}, {"unconscious": True}]},
        {"is_accepting": True, "patients": [{}]},
    ]
    assert process_triage_wards(wards, 10) == {
        "acuity_score": 35, "status": "TRIAGE_STABLE"}


@pytest.mark.parametrize("wards,score", [([], 10), ([{"is_accepting": True}], 10),
                                        ([{"is_accepting": True, "patients": [{}]}], 0)])
def test_empty_and_zero_acuity(wards, score):
    assert process_triage_wards(wards, score) == {
        "acuity_score": 0, "status": "NO_URGENT_CASES"}


@pytest.mark.parametrize("streams,expected", [
    (None, "NO_DATA"), ([], "NO_DATA"), ([[]], "PRESSURE_NORMAL"),
    ([[3.9], [3.9]], "PRESSURE_NORMAL"),
    ([[3.9, 4.0, 3.9]], "PRESSURE_NORMAL"),
    ([[4.0, 4.1]], "PRESSURE_NORMAL"),
    ([[], [3.9, 3.9]], "PRESSURE_FAILURE"),
])
def test_oxygen_boundaries_and_manifold_isolation(streams, expected):
    assert monitor_oxygen_manifolds(streams) == expected
