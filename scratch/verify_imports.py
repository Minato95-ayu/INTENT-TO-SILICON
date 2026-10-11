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

import os, ast, sys

tests_dir = r"D:\INTENT-TO-SILICON\tests"
missing_modules = [
    "compiler.frontend", 
    "tools.package_manager", 
    "runtime.vm.handlers.math", 
    "runtime.vm.handlers.logic", 
    "runtime.vm_next", 
    "runtime.ui.runtime",
    "compiler.backend.html_generator",
    "runtime.http.runtime",
    "runtime.stdlib",
    "runtime.vm.instructions"
]

results = []

for root, _, files in os.walk(tests_dir):
    for f in files:
        if not f.endswith(".py"): continue
        path = os.path.join(root, f)
        
        try:
            with open(path, "r", encoding="utf8") as file:
                source = file.read()
            tree = ast.parse(source)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    mod = node.module or ""
                    for missing in missing_modules:
                        if mod.startswith(missing):
                            names = [alias.name for alias in node.names]
                            results.append(f"{f} imports {names} from {mod}")
        except SyntaxError as e:
            results.append(f"SYNTAX_ERROR in {f}: {e}")
        except Exception as e:
            results.append(f"ERROR reading {f}: {e}")

for r in set(results):
    print(r)
