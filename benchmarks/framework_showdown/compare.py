import os
import glob

def count_loc(directory, extensions):
    total_loc = 0
    total_files = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # ignore empty lines and comments
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#') and not line.startswith('//'):
                            total_loc += 1
                total_files += 1
    return total_loc, total_files

aayu_loc, aayu_files = count_loc("aayu_app", [".aayu"])
fastapi_loc, fastapi_files = count_loc("fastapi_app", [".py"])
django_loc, django_files = count_loc("django_app", [".py"])

print("=== FRAMEWORK SHOWDOWN: BOILERPLATE METRICS ===")
print(f"FastAPI App : {fastapi_loc} LOC across {fastapi_files} files.")
print(f"Django App  : {django_loc} LOC across {django_files} files.")
print(f"AAYU App    : {aayu_loc} LOC across {aayu_files} files.")
print(f"Reduction vs FastAPI : {((fastapi_loc - aayu_loc) / fastapi_loc) * 100:.1f}% less code in AAYU")
print(f"Reduction vs Django  : {((django_loc - aayu_loc) / django_loc) * 100:.1f}% less code in AAYU")

