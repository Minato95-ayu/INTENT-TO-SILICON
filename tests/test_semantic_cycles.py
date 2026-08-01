import pytest
import sys
import os

# Add root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aayu.compiler.ast.nodes import ProgramNode, ImportNode
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.errors import CompilerError

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
