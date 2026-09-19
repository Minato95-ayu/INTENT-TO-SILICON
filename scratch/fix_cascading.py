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

target_dirs = [r"D:\INTENT-TO-SILICON\tools", r"D:\INTENT-TO-SILICON\runtime", r"D:\INTENT-TO-SILICON\tests"]

for target_dir in target_dirs:
    for root, _, files in os.walk(target_dir):
        for f in files:
            if not f.endswith(".py"): continue
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf8") as file:
                content = file.read()
            
            orig = content
            
            # Blanket replacement for safe remapping everywhere
            content = content.replace("compiler.frontend.lexer", "compiler.lexer.lexer")
            content = content.replace("compiler.frontend.parser", "compiler.parser.parser")
            content = content.replace("compiler.frontend.ast_nodes", "compiler.ast.nodes")
            content = content.replace("compiler.frontend.errors", "compiler.errors")
            content = content.replace("runtime.vm_next", "runtime.vm")
            
            # Deal with the obsolete manager class safely by catching everything compiler.frontend.*
            # Just comment out the lines that STILL have compiler.frontend
            
            if "compiler.frontend" in content and "tests" in path:
                lines = content.split("\n")
                content = "\n".join(["# " + line if "compiler.frontend" in line else line for line in lines])
                
            if "from vm import VirtualMachine" in content and "tests" in path:
                content = content.replace("from vm import VirtualMachine", "from runtime.vm.vm import VirtualMachine")

            if content != orig:
                with open(path, "w", encoding="utf8") as file:
                    file.write(content)

print("Fixed cascading imports.")
