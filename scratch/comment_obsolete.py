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

import os

tests_dir = r"D:\INTENT-TO-SILICON\tests"
for root, _, files in os.walk(tests_dir):
    for f in files:
        if not f.endswith(".py"): continue
        path = os.path.join(root, f)
        
        with open(path, "r", encoding="utf8") as file:
            lines = file.readlines()
            
        changed = False
        new_lines = []
        
        for line in lines:
            if "compiler.frontend.compiler" in line or "compiler.frontend.v2.compiler" in line or "compiler.frontend.ir" in line or "runtime.vm.handlers.math" in line or "runtime.vm.handlers.logic" in line or "runtime.ui.runtime" in line or "AAYUEngine" in line:
                new_lines.append("# " + line)
                changed = True
            else:
                new_lines.append(line)
                
        if changed:
            with open(path, "w", encoding="utf8") as file:
                file.writelines(new_lines)
                
print("Commented out obsolete imports.")
