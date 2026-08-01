from typing import Optional
from aayu.compiler.ast.nodes import ProgramNode
from aayu.compiler.semantic.diagnostics import DiagnosticEngine, engine as global_diag_engine
from aayu.compiler.semantic.scope_pass import ScopePass
from aayu.compiler.semantic.symbol_pass import SymbolPass
from aayu.compiler.semantic.type_pass import TypePass
from aayu.compiler.semantic.constant_pass import ConstantPass
from aayu.compiler.semantic.nodes import SemanticProgramNode
from aayu.compiler.semantic.analyzer import SemanticAnalyzer

class SemanticPipeline:
    """
    Phase 12.0 Semantic Pipeline Orchestrator
    Executes AST validation and transformation passes in strict order.
    Returns an immutable HIR (SemanticProgramNode) if successful.
    """
    def __init__(self, diag_engine: DiagnosticEngine = None):
        self.diag_engine = diag_engine or global_diag_engine

    def run(self, ast: ProgramNode) -> Optional[SemanticProgramNode]:
        self.diag_engine.clear()

        # 1. Scope Builder Pass
        scope_pass = ScopePass(self.diag_engine)
        scope_pass.run(ast)
        if self.diag_engine.has_errors():
            return None

        # 2. Symbol Resolver Pass
        symbol_pass = SymbolPass(self.diag_engine, scope_pass)
        symbol_pass.run(ast)
        if self.diag_engine.has_errors():
            return None

        # 3. Type Resolver Pass
        type_pass = TypePass(self.diag_engine, scope_pass)
        type_pass.run(ast)
        if self.diag_engine.has_errors():
            return None

        # 4. Constant Evaluator Pass
        constant_pass = ConstantPass(self.diag_engine, scope_pass)
        ast = constant_pass.run(ast)
        if self.diag_engine.has_errors():
            return None

        # 5. Build Immutable HIR
        # Temporarily use the old SemanticAnalyzer to build SemanticNodes for now,
        # but with a clean AST that has been pre-verified and constant-folded.
        # Future phases will replace this with a dedicated HIRBuilder.
        analyzer = SemanticAnalyzer()
        hir = analyzer.analyze(ast)
        return hir
