"""
=============================================================================
FILE: fix_imports.py
PURPOSE: Fixes import issues
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles fixes import issues.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os
import glob

def fix_imports(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('from .parser import', 'from intent_engine.nlp.parser import')
    content = content.replace('from ..ir.nodes import', 'from intent_engine.ir.nodes import')
    content = content.replace('from ..graphs.intent_graph import', 'from intent_engine.graphs.intent_graph import')
    content = content.replace('from .graphs.intent_graph import', 'from intent_engine.graphs.intent_graph import')
    content = content.replace('from .graphs.architecture_graph import', 'from intent_engine.graphs.architecture_graph import')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

base = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine'
fix_imports(os.path.join(base, 'nlp', 'detectors.py'))
fix_imports(os.path.join(base, 'clarification', 'clarification_engine.py'))
fix_imports(os.path.join(base, 'architecture_generator.py'))
fix_imports(os.path.join(base, 'code_planner.py'))
