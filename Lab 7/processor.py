"""Input-safe versions of the three Lab 7 parsers.

Invalid vitals/allocation return a descriptive string; invalid BMI returns None.
These are assignment rules, not a clinical triage system.
"""
import math
import re

INVALID_VITALS = "Invalid vitals summary"
INVALID_ALLOCATION = "Invalid ward allocation"
WARD_NAMES = {
    "ER": "Emergency Room",
    "ICU": "Intensive Care Unit",
    "GEN": "General Ward",
    "PED": "Pediatrics",
}
MAX_INPUT_LENGTH = 1000


def _parts(value, delimiter, count):
    if not isinstance(value, str) or len(value) > MAX_INPUT_LENGTH:
        return None
    parts = [part.strip() for part in value.split(delimiter)]
    if len(parts) != count or any(not part for part in parts):
        return None
    return parts


def _finite_numbers(parts):
    try:
        numbers = tuple(float(part) for part in parts)
    except (ValueError, OverflowError):
        return None
    return numbers if all(math.isfinite(number) for number in numbers) else None


def parse_vitals_summary(vitals_csv):
    """Parse HR,SpO2,Temp; reject non-finite values and invalid domains.

    HR must be positive, SpO2 in (0, 100], and Celsius temperature positive.
    The starter's critical thresholds and valid-output format are preserved.
    """
    parts = _parts(vitals_csv, ',', 3)
    if parts is None:
        return INVALID_VITALS
    numbers = _finite_numbers(parts)
    if numbers is None:
        return INVALID_VITALS
    hr, spo2, temp = numbers
    if hr <= 0 or not 0 < spo2 <= 100 or temp <= 0:
        return INVALID_VITALS
    critical = hr > 120 or spo2 < 90 or temp > 39.0
    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"


def compute_patient_bmi(bmi_string):
    """Return rounded BMI for positive finite kg/metres, otherwise None.

    Reject overflow and floating point underflow rather than returning a
    misleading zero, infinity, NaN, or an uncaught arithmetic exception.
    """
    parts = _parts(bmi_string, '/', 2)
    if parts is None:
        return None
    numbers = _finite_numbers(parts)
    if numbers is None:
        return None
    weight, height = numbers
    if weight <= 0 or height <= 0:
        return None
    try:
        squared = height ** 2
        bmi = weight / squared
    except (OverflowError, ZeroDivisionError):
        return None
    if not math.isfinite(bmi) or bmi <= 0:
        return None
    result = round(bmi, 2)
    return result if result > 0 else None


def assign_ward_bed(allocation_code):
    """Accept a known ward plus a positive ASCII bed integer (e.g. ICU-05)."""
    parts = _parts(allocation_code, '-', 2)
    if parts is None:
        return INVALID_ALLOCATION
    ward, bed_str = parts
    ward = ward.upper()
    if ward not in WARD_NAMES or re.fullmatch(r'[0-9]+', bed_str) is None:
        return INVALID_ALLOCATION
    bed_num = int(bed_str)
    if bed_num <= 0:
        return INVALID_ALLOCATION
    return f"{WARD_NAMES[ward]} Bed #{bed_num}"


def main():
    try:
        print("==== Running parse_vitals_summary ====")
        v_input = input("Enter vitals (HR,SpO2,Temp): ")
        print("Summary:", parse_vitals_summary(v_input))
        print("\n==== Running compute_patient_bmi ====")
        b_input = input("Enter weight/height (e.g. 70/1.75): ")
        bmi = compute_patient_bmi(b_input)
        print("BMI:", bmi if bmi is not None else "Invalid BMI input")
        print("\n==== Running assign_ward_bed ====")
        w_input = input("Enter allocation (e.g. ICU-05): ")
        print("Assignment:", assign_ward_bed(w_input))
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")


if __name__ == '__main__':
    main()
