import glob
import re
import os

files = glob.glob("tests/**/*.py", recursive=True)
skipped_files = []

for f in files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
        if "pytest.mark.skip" in content or "@unittest.skip" in content:
            skipped_files.append(f)

for sf in skipped_files:
    print(f"File: {sf}")
    with open(sf, "r", encoding="utf-8") as file:
        lines = file.readlines()
        test_names = [l.strip() for l in lines if l.strip().startswith("def test_")]
        print(f"Tests: {len(test_names)}")
        for tn in test_names[:5]:
            print(f"  - {tn}")
        if len(test_names) > 5:
            print("  ...")
    print()
