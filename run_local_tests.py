# -*- coding: utf-8 -*-
"""
הרצת טסטים מקומית שמדמה בדיוק את מה ש-VPL עושה:
מריצה את Adapters/main.py כתהליך נפרד (subprocess), מזינה לו קלט בפורמט
Board:/Commands: דרך ה-stdin שלו, ותופסת את מה שהוא מדפיס בפועל.

*** איך להריץ ***
1. להעתיק את הקובץ הזה ואת cases.py לתוך תיקיית השורש של הפרויקט
   (אותה תיקייה שבה נמצא config.py, וגם Adapters/ ו-Entities/ וכו').
2. מהטרמינל, מתוך אותה תיקייה:
       python run_local_tests.py
   (אם יש כמה גרסאות פייתון אצלך, אולי תצטרכי python3 run_local_tests.py)

הסקריפט ירוץ עם python (sys.executable), בדיוק כמו הרצה רגילה של main.py,
כדי לגלות כבר עכשיו אם יש בעיות ייבוא (import) לפני שמעלים ל-VPL.
"""

import subprocess
import sys
import os

from cases import TEST_CASES

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(PROJECT_ROOT, "Adapters", "main.py")


def normalize(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    return "\n".join(lines)


def run_case(name, input_text, expected_output):
    result = subprocess.run(
        [sys.executable, MAIN_SCRIPT],
        input=input_text,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    actual_output = result.stdout
    had_error = result.returncode != 0 or bool(result.stderr.strip())

    passed = (not had_error) and (normalize(actual_output) == normalize(expected_output))

    print("=" * 70)
    print(f"Test: {name}")
    print("PASSED" if passed else "FAILED")

    if not passed:
        print("--- Input ---")
        print(input_text)
        print("--- Program output (stdout) ---")
        print(actual_output if actual_output.strip() else "(empty)")
        if result.stderr.strip():
            print("--- Program errors (stderr) ---")
            print(result.stderr)
        print("--- Expected output (exact text) ---")
        print(expected_output)

    return passed


def main():
    if not os.path.isfile(MAIN_SCRIPT):
        print(f"לא נמצא הקובץ: {MAIN_SCRIPT}")
        print("ודאי שהעתקת את run_local_tests.py ו-cases.py לתוך תיקיית השורש של הפרויקט (ליד config.py).")
        sys.exit(1)

    total = len(TEST_CASES)
    passed_count = 0

    for name, input_text, expected_output in TEST_CASES:
        if run_case(name, input_text, expected_output):
            passed_count += 1

    print("=" * 70)
    print(f"תוצאה סופית: {passed_count}/{total} טסטים עברו")


if __name__ == "__main__":
    main()
