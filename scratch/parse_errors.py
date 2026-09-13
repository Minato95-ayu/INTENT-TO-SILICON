import re
from collections import defaultdict

with open(r"D:\INTENT-TO-SILICON\scratch\collection_errors.log", "r", encoding="utf8", errors="ignore") as f:
    content = f.read()

# We look for blocks starting with "ERROR tests/..." and find the corresponding "E   ..." line
errors = defaultdict(list)
blocks = content.split("________ ERROR collecting")

for block in blocks[1:]:
    # Find the test file name
    lines = block.strip().split("\n")
    test_file_match = re.search(r"tests[/\\]\S+", lines[0])
    test_file = test_file_match.group(0) if test_file_match else "unknown"
    
    # Find the Error line
    error_line = "Unknown Error"
    for line in lines:
        if line.startswith("E   "):
            error_line = line[4:].strip()
            break
            
    errors[error_line].append(test_file)

print(f"{'Count':<6} | {'Error Type':<70}")
print("-" * 80)
for err_type, files in sorted(errors.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"{len(files):<6} | {err_type[:70]}")
    for f in files[:3]:
        print(f"       - {f}")
    if len(files) > 3:
        print(f"       - ... and {len(files)-3} more")
