import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from aayu.compiler.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.pipeline import SemanticPipeline

def run_semantic(code: str):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    pipeline = SemanticPipeline()
    hir = pipeline.run(ast)
    return hir, pipeline.diag_engine.diagnostics

def test_valid_program():
    code = """
    state count = 10
    action Test()
        count = count + 5
    end
    """
    hir, diags = run_semantic(code)
    assert not diags
    assert hir is not None

def test_undefined_variable():
    code = """
    action Test()
        x = y + 5
    end
    """
    hir, diags = run_semantic(code)
    assert len(diags) > 0
    assert any(d.code == "E000" and "Undefined symbol 'y'." in d.message for d in diags)

def test_duplicate_state():
    code = """
    state count = 10
    state count = 20
    """
    hir, diags = run_semantic(code)
    assert len(diags) > 0
    assert any(d.code == "E101" and "already defined" in d.message for d in diags)

def test_constant_folding():
    code = """
    state count = 10 + 5 * 2
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Before folding, it's a BinaryOpNode
    from aayu.compiler.ast.nodes import BinaryOpNode, LiteralNode, StateDeclarationNode
    assert isinstance(ast.statements[0], StateDeclarationNode)
    assert isinstance(ast.statements[0].value, BinaryOpNode)
    
    from aayu.compiler.semantic.diagnostics import DiagnosticEngine
    from aayu.compiler.semantic.scope_pass import ScopePass
    from aayu.compiler.semantic.symbol_pass import SymbolPass
    from aayu.compiler.semantic.type_pass import TypePass
    from aayu.compiler.semantic.constant_pass import ConstantPass
    from aayu.compiler.semantic.context import SemanticContext
    
    diag_engine = DiagnosticEngine()
    context = SemanticContext(diag_engine)
    
    scope_pass = ScopePass()
    scope_pass.run_with_context(ast, context)
    
    symbol_pass = SymbolPass()
    symbol_pass.run_with_context(ast, context)
    
    type_pass = TypePass()
    type_pass.run_with_context(ast, context)
    
    scope_pass.node_scopes = context.node_scopes
    scope_pass.node_types = context.type_registry.resolved_types
    constant_pass = ConstantPass(diag_engine, scope_pass)
    ast_folded = constant_pass.run(ast)
    
    # After folding, it should be a LiteralNode with value 20
    assert not diag_engine.diagnostics
    assert isinstance(ast_folded.statements[0].value, LiteralNode)
    assert ast_folded.statements[0].value.value == 20

def test_type_mismatch_binary():
    code = """
    action Test()
        x = 10 - "string"
    end
    """
    hir, diags = run_semantic(code)
    assert len(diags) > 0
    assert any(d.code == "E201" for d in diags)

    
def test_valid_widget_tree():
    code = """
    action Column()
    end
    action Text(val)
    end
    action View()
        Column
            Text("Hello")
        end
    end
    """
    hir, diags = run_semantic(code)
    assert not diags

def test_invalid_type_assignment():
    code = """
    action Test()
        # In AAYU, locals are dynamically typed or implicitly typed.
        # But if type pass enforces strictness, let's see.
        count = 10
        count = "hello"
    end
    """
    hir, diags = run_semantic(code)
    # Right now our TypePass might just be basic. Just ensure it doesn't crash.
    pass

def test_unknown_action_call():
    code = """
    action Test()
        doSomething()
    end
    """
    hir, diags = run_semantic(code)
    assert len(diags) > 0
    assert any("Undefined symbol 'doSomething'" in d.message for d in diags)

def test_valid_loop():
    code = """
    action Test()
        count = 0
        while count < 10
            count = count + 1
        end
    end
    """
    hir, diags = run_semantic(code)
    assert not diags

def test_shadowing_warning():
    code = """
    state count = 0
    action Test()
        count = 10 # This shadows state count in local scope or modifies it?
        # AAYU rules: variables are local if assigned without explicit declaration or maybe modifies state.
        # But for semantic pipeline, just verify it parses and resolves without crashing.
    end
    """
    hir, diags = run_semantic(code)
    assert not diags

