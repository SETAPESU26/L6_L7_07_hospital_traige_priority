"""Line coverage suite for the unchanged assignment application."""
import pytest
from hospital_triage_priority import monitor_oxygen_manifolds, process_triage_wards


def ward(patients, **options):
    return {"is_accepting": True, "patients": patients, **options}


@pytest.mark.parametrize("wards,score", [(None, 10), ({}, 10), ([], -1)])
def test_invalid_arguments(wards, score):
    with pytest.raises(ValueError, match="Invalid wards list or base acuity score"):
        process_triage_wards(wards, score)


def test_closed_ward_is_skipped():
    assert process_triage_wards([{"patients": [{"unconscious": True}]}], 10) == {
        "acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_general_ward_patient_paths_and_standby():
    patients = [{"spo2": 0}, {"unconscious": True}, {"spo2": 89}, {}]
    assert process_triage_wards([ward(patients, icu_standby=True)], 10) == {
        "acuity_score": 195, "status": "TRIAGE_STABLE"}


def test_outpatient_unconscious_resets_score_and_stops_patients():
    wards = [ward([{}]), ward([{"unconscious": True}, {}], tier="outpatient")]
    assert process_triage_wards(wards, 10) == {
        "acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_five_invalid_patients_trigger_alert():
    assert process_triage_wards([ward([{"hr": 0}] * 5)], 10) == {
        "acuity_score": 0, "status": "WARD_ALERT"}


def test_oxygen_no_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_oxygen_normal_resets_streak():
    assert monitor_oxygen_manifolds([[3.9, 4.0, 3.9]]) == "PRESSURE_NORMAL"


def test_oxygen_failure():
    assert monitor_oxygen_manifolds([[4.0, 3.9, 3.8]]) == "PRESSURE_FAILURE"
