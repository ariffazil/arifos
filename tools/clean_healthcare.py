#!/usr/bin/env python3
"""
Thermodynamic Data Cleaner — healthcare_messy_data.csv
-------------------------------------------------------
Principle: Entropy reduction. Every transformation moves the dataset
from a high-disorder (high-S) state toward a canonical low-entropy form.

S_field = -Σ p(value) * log2 p(value)  ← Shannon entropy per column

Cleaning stages mirror thermodynamic phases:
  Phase 0 — INTAKE        : load raw, measure initial entropy
  Phase 1 — CONDENSATION  : collapse whitespace, normalise casing
  Phase 2 — CRYSTALLISATION: resolve mixed types (Age "forty" → 40)
  Phase 3 — DISTILLATION  : unify date formats → ISO 8601
  Phase 4 — FILTRATION    : standardise NaN representations
  Phase 5 — EQUILIBRIUM   : split Blood Pressure into components
  Phase 6 — SEAL          : output clean CSV + entropy report
"""

import csv
import io
import math
import re
import sys
import urllib.request
from collections import Counter
from datetime import datetime

URL = "https://raw.githubusercontent.com/eyowhite/Messy-dataset/main/healthcare_messy_data.csv"

# ── Helpers ────────────────────────────────────────────────────────────────────

WORD_TO_NUM = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90, "hundred": 100,
}

DATE_FORMATS = [
    "%m/%d/%Y",      # 01/15/2020
    "%Y/%m/%d",      # 2020/02/20
    "%Y.%m.%d",      # 2019.12.01
    "%m-%d-%Y",      # 03-25-2019
    "%B %d, %Y",     # April 5, 2018
    "%B %d %Y",      # April 5 2018
    "%Y-%m-%d",      # 2020-01-15  (already ISO)
]

NULL_TOKENS = {"nan", "none", "null", "n/a", "na", "", " "}


def shannon_entropy(values: list) -> float:
    """Shannon entropy of a column (bits). Higher = more disorder."""
    counts = Counter(str(v).strip().lower() for v in values)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counts.values() if c > 0)


def is_null(val: str) -> bool:
    return str(val).strip().lower() in NULL_TOKENS


def clean_age(raw: str) -> str:
    raw = raw.strip().lower()
    if is_null(raw):
        return ""
    # Try direct int
    try:
        return str(int(float(raw)))
    except ValueError:
        pass
    # Try word → number (handles "forty", "forty five", etc.)
    parts = raw.split()
    total = 0
    for part in parts:
        n = WORD_TO_NUM.get(part)
        if n is None:
            return ""  # unknown word form
        total += n
    return str(total) if total else ""


def parse_date(raw: str) -> str:
    raw = raw.strip()
    if is_null(raw):
        return ""
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw  # keep unparseable as-is; flag later


def clean_bp(raw: str) -> tuple[str, str]:
    """Return (systolic, diastolic) or ('', '')."""
    raw = raw.strip()
    if is_null(raw):
        return "", ""
    m = re.match(r"(\d+)\s*/\s*(\d+)", raw)
    if m:
        return m.group(1), m.group(2)
    return "", ""


def clean_phone(raw: str) -> str:
    raw = raw.strip()
    if is_null(raw):
        return ""
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    if len(digits) == 11 and digits[0] == "1":
        return f"{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    return raw  # keep non-standard as-is


def clean_email(raw: str) -> str:
    raw = raw.strip()
    if is_null(raw):
        return ""
    # basic sanity: must contain @
    return raw if "@" in raw else ""


def clean_gender(raw: str) -> str:
    r = raw.strip().lower()
    if r in ("male", "m"):
        return "Male"
    if r in ("female", "f"):
        return "Female"
    if r in ("other", "o", "non-binary", "nonbinary"):
        return "Other"
    return raw.strip().title() if raw.strip() else ""


def clean_condition(raw: str) -> str:
    r = raw.strip()
    # "None" as a condition means no diagnosis recorded
    if r.lower() in ("none", "nan", ""):
        return ""
    return r.title()


def clean_medication(raw: str) -> str:
    r = raw.strip()
    if r.lower() in ("none", "nan", ""):
        return ""
    return r.upper()


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    # ── Phase 0: INTAKE ────────────────────────────────────────────────────────
    sys.stderr.write("Phase 0 — INTAKE: downloading dataset…\n")
    with urllib.request.urlopen(URL) as resp:
        raw_text = resp.read().decode("utf-8")

    reader = csv.DictReader(io.StringIO(raw_text))
    rows = list(reader)
    sys.stderr.write(f"         {len(rows)} records loaded.\n")

    # Measure initial entropy per column
    col_names = reader.fieldnames or []
    initial_entropy = {c: shannon_entropy([r[c] for r in rows]) for c in col_names}

    # ── Phases 1–5: TRANSFORMATION ─────────────────────────────────────────────
    cleaned = []
    stats = {
        "age_fixed": 0, "date_unified": 0, "bp_split": 0,
        "nulls_cleared": 0, "phone_normalised": 0,
    }

    for row in rows:
        name = row["Patient Name"].strip().title()

        age_raw = row["Age"]
        age = clean_age(age_raw)
        if not is_null(age_raw) and age_raw.strip().lower() not in ("nan",) and age != age_raw.strip():
            stats["age_fixed"] += 1

        gender = clean_gender(row["Gender"])
        condition = clean_condition(row["Condition"])
        medication = clean_medication(row["Medication"])

        date_raw = row["Visit Date"].strip()
        date_iso = parse_date(date_raw)
        if date_iso and date_iso != date_raw:
            stats["date_unified"] += 1

        sys_bp, dia_bp = clean_bp(row["Blood Pressure"])
        if sys_bp:
            stats["bp_split"] += 1

        cholesterol = row["Cholesterol"].strip()
        cholesterol = "" if is_null(cholesterol) else cholesterol

        email = clean_email(row["Email"])
        phone = clean_phone(row["Phone Number"])

        # Count nulls cleared
        raw_nulls = sum(1 for v in row.values() if is_null(v))
        new_nulls = sum(1 for v in [name, age, gender, condition, medication,
                                    date_iso, sys_bp, dia_bp, cholesterol, email, phone]
                        if v == "")
        stats["nulls_cleared"] += max(0, raw_nulls - new_nulls)

        cleaned.append({
            "Patient Name": name,
            "Age": age,
            "Gender": gender,
            "Condition": condition,
            "Medication": medication,
            "Visit Date": date_iso,
            "BP Systolic": sys_bp,
            "BP Diastolic": dia_bp,
            "Cholesterol": cholesterol,
            "Email": email,
            "Phone Number": phone,
        })

    # ── Phase 6: SEAL ──────────────────────────────────────────────────────────
    out_fields = ["Patient Name", "Age", "Gender", "Condition", "Medication",
                  "Visit Date", "BP Systolic", "BP Diastolic", "Cholesterol",
                  "Email", "Phone Number"]

    out_path = "/srv/arifOS/tools/healthcare_clean.csv"
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(cleaned)

    # Entropy report
    final_entropy = {c: shannon_entropy([r[c] for r in cleaned]) for c in out_fields
                     if c in ("Age", "Gender", "Condition", "Medication",
                               "Visit Date", "BP Systolic", "BP Diastolic")}

    # Map old column names to new for comparison
    entropy_map = {
        "Age": "Age", "Gender": "Gender", "Condition": "Condition",
        "Medication": "Medication", "Visit Date": "Visit Date",
    }

    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║         THERMODYNAMIC ENTROPY REPORT — arifOS Cleaner        ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Records processed : {len(rows):<39}║")
    print(f"║  Output file       : healthcare_clean.csv{'':<19}║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  TRANSFORMATION LOG                                          ║")
    print(f"║  Age words → integers  : {stats['age_fixed']:<35}║")
    print(f"║  Dates → ISO 8601      : {stats['date_unified']:<35}║")
    print(f"║  BP split (sys/dia)    : {stats['bp_split']:<35}║")
    print(f"║  Nulls resolved        : {stats['nulls_cleared']:<35}║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  ENTROPY DELTA (bits per column, lower = more ordered)       ║")
    print(f"║  {'Column':<20} {'Before':>8} {'After':>8} {'ΔS':>8}     ║")
    print("║  " + "─" * 56 + "  ║")
    for col, new_col in entropy_map.items():
        if col in initial_entropy and new_col in final_entropy:
            s0 = initial_entropy[col]
            s1 = final_entropy[new_col]
            delta = s1 - s0
            arrow = "▼" if delta < 0 else ("▲" if delta > 0 else "─")
            print(f"║  {col:<20} {s0:>8.3f} {s1:>8.3f} {delta:>+8.3f} {arrow}   ║")
    # BP (new columns)
    for bp_col in ("BP Systolic", "BP Diastolic"):
        s1 = final_entropy.get(bp_col, 0)
        print(f"║  {bp_col:<20} {'(split)':>8} {s1:>8.3f} {'new':>8}     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"\nClean data written to: {out_path}")


if __name__ == "__main__":
    main()
