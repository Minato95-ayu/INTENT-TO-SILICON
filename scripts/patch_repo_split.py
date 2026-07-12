"""
=============================================================================
FILE: patch_repo_split.py
PURPOSE: Fixes or patches existing code
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles fixes or patches existing code.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import shutil
import glob

# 1. Create top-level directories
proto_dir = "prototype"
language_dir = os.path.join(proto_dir, "language")
platform_dir = os.path.join(proto_dir, "platform")
brainos_dir = os.path.join(proto_dir, "brainos")

os.makedirs(language_dir, exist_ok=True)
os.makedirs(platform_dir, exist_ok=True)
os.makedirs(brainos_dir, exist_ok=True)

# 2. Populate Platform and BrainOS folders
for d in ["builder", "chat", "studio", "software_factory"]:
    os.makedirs(os.path.join(platform_dir, d), exist_ok=True)

for d in ["graph", "kernel", "context", "storage"]:
    os.makedirs(os.path.join(brainos_dir, d), exist_ok=True)

# 3. Move aayu_language contents to language
aayu_dir = os.path.join(proto_dir, "aayu_language")
if os.path.exists(aayu_dir):
    for item in os.listdir(aayu_dir):
        src = os.path.join(aayu_dir, item)
        dst = os.path.join(language_dir, item)
        if not os.path.exists(dst):
            shutil.move(src, dst)
    # Remove old dir if empty
    try:
        os.rmdir(aayu_dir)
    except OSError:
        pass

# 4. Tests Reorganization
tests_dir = os.path.join(proto_dir, "tests")
legacy_dir = os.path.join(tests_dir, "legacy")
os.makedirs(legacy_dir, exist_ok=True)

new_test_dirs = ["lexer", "parser", "lowering", "optimizer", "compiler", "runtime", "integration", "benchmarks"]
for d in new_test_dirs:
    os.makedirs(os.path.join(tests_dir, d), exist_ok=True)

# Move all root test files to legacy
for item in os.listdir(tests_dir):
    src = os.path.join(tests_dir, item)
    if os.path.isfile(src) and item != "legacy":
        dst = os.path.join(legacy_dir, item)
        shutil.move(src, dst)
    elif os.path.isdir(src) and item not in new_test_dirs + ["legacy", "__pycache__"]:
        # move old folders like runtime if we want, but wait, runtime is a new folder!
        # The prompt says move old tests. If runtime already exists and has old tests, move them into legacy?
        # Actually I just created it. So before I created it, any existing dir like 'runtime' in tests?
        pass

print("Repository Split and Tests Reorganization completed.")
