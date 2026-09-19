# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import os, re, sys
from collections import defaultdict

log_file = r"D:\INTENT-TO-SILICON\scratch\collection_errors.log"
with open(log_file, "r", encoding="utf8", errors="ignore") as f:
    content = f.read()

blocks = content.split("________ ERROR collecting")
errors = {}

for block in blocks[1:]:
    lines = block.strip().split("\n")
    test_file_match = re.search(r"tests[/\\]\S+", lines[0])
    if not test_file_match: continue
    test_file = test_file_match.group(0).strip()
    
    error_line = "Unknown"
    for line in lines:
        if line.startswith("E   "):
            error_line = line[4:].strip()
            break
    errors[test_file] = error_line

print(f"Found {len(errors)} failing files.")

# Let's map out what they are importing for compiler.frontend
print("\n--- FRONTEND API PROOFING ---")
frontend_imports = []
for fpath, err in errors.items():
    if "compiler.frontend" in err:
        full_path = os.path.join(r"D:\INTENT-TO-SILICON", fpath)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf8") as f:
                content = f.read()
                imports = re.findall(r"from compiler\.frontend\.\w+\s+import\s+(.+)", content)
                for imp in imports:
                    frontend_imports.extend([i.strip() for i in imp.split(",")])

print("Unique Classes/Symbols expected by tests from compiler.frontend.* :")
for sym in set(frontend_imports):
    print(f" - {sym}")

print("\n--- OTHER ERRORS ---")
for fpath, err in errors.items():
    if "compiler.frontend" not in err:
        print(f"{fpath} -> {err}")

