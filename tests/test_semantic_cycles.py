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

import pytest
import sys
import os

# Add root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from compiler.ast.nodes import ProgramNode, ImportNode
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.errors import CompilerError

def test_import_cycle_detection():
    # Program: import A
    ast_A = ProgramNode(line=1, column=1, statements=[
        ImportNode(line=1, column=1, module="A")
    ])
    
    # Pre-seed visited_modules with 'A' to simulate A being the current context
    analyzer = SemanticAnalyzer(visiting_modules={"A"})
    
    with pytest.raises(CompilerError) as excinfo:
        analyzer.analyze(ast_A)
        
    assert "Import cycle detected: 'A'" in str(excinfo.value)

if __name__ == '__main__':
    pytest.main(['-v', __file__])
