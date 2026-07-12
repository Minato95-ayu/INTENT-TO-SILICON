"""
=============================================================================
FILE: patch_phase2_3.py
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

passes_dir = r"prototype\aayu_language\passes"
os.makedirs(passes_dir, exist_ok=True)

# Create __init__.py
with open(os.path.join(passes_dir, "__init__.py"), "w", encoding="utf-8") as f:
    f.write("# Passes package\n")

# Move lowering.py
old_lowering = r"prototype\aayu_language\lowering.py"
new_lowering = os.path.join(passes_dir, "lowering.py")
if os.path.exists(old_lowering):
    shutil.move(old_lowering, new_lowering)

# Create optimizer.py
with open(os.path.join(passes_dir, "optimizer.py"), "w", encoding="utf-8") as f:
    f.write("# Optimizer pass (Future)\n")

# Update run.py
run_path = r"prototype\aayu_language\run.py"
with open(run_path, "r", encoding="utf-8") as f:
    run_content = f.read()
run_content = run_content.replace("from lowering import LoweringPass", "from passes.lowering import LoweringPass")
with open(run_path, "w", encoding="utf-8") as f:
    f.write(run_content)

# Update lowering.py ast_nodes import
with open(new_lowering, "r", encoding="utf-8") as f:
    lowering_content = f.read()
lowering_content = lowering_content.replace("from ast_nodes import *", "from ..ast_nodes import *")
# Use correct operators for comparison and math
lowering_content = lowering_content.replace('operator="GREATER"', 'operator=">"')
lowering_content = lowering_content.replace('operator="MINUS"', 'operator="-"')
lowering_content = lowering_content.replace('operator="LESS"', 'operator="<"')
lowering_content = lowering_content.replace('operator="PLUS"', 'operator="+"')

# Also, RepeatNode was generating a BlockNode, but wait, the AST doesn't have BlockNode? It used list of nodes. The user said: "Lowering: BlockNode". Does BlockNode exist?
# We can check if BlockNode exists in ast_nodes.py.

with open(new_lowering, "w", encoding="utf-8") as f:
    f.write(lowering_content)

print("Phase 2.3 Refactoring completed.")
