from typing import Optional
from aayu.compiler.ast.nodes import ProgramNode
from aayu.compiler.semantic.diagnostics import DiagnosticEngine, engine as global_diag_engine
from aayu.compiler.semantic.scope_pass import ScopePass
from aayu.compiler.semantic.symbol_pass import SymbolPass
from aayu.compiler.semantic.type_pass import TypePass
from aayu.compiler.semantic.constant_pass import ConstantPass
from aayu.compiler.hir.nodes import HIRModule
from aayu.compiler.hir.builder import HIRBuilder

class SemanticPipeline:
    """
    Phase 12.0 Semantic Pipeline Orchestrator
    Executes AST validation and transformation passes in strict order.
    Returns an immutable HIR (HIRModule) if successful.
    """
    def __init__(self, diag_engine: DiagnosticEngine = None):
        self.diag_engine = diag_engine or global_diag_engine
        
        # Expose passes so they can be run individually or accessed (e.g. for testing)
        self.scope_pass = None
        self.symbol_pass = None
        self.type_pass = None
        self.constant_pass = None

    def run(self, ast: ProgramNode) -> Optional[HIRModule]:
        self.diag_engine.clear()

        # 1. Scope Builder Pass
        from aayu.compiler.semantic.context import SemanticContext
        self.context = SemanticContext(self.diag_engine)
        self.scope_pass = ScopePass()
        self.scope_pass.run_with_context(ast, self.context)
        if self.diag_engine.has_errors():
            return None

        # 2. Symbol Resolver Pass
        self.symbol_pass = SymbolPass()
        self.symbol_pass.run_with_context(ast, self.context)
        if self.diag_engine.has_errors():
            return None

        # 3. Type Resolver Pass
        self.type_pass = TypePass()
        self.type_pass.run_with_context(ast, self.context)
        if self.diag_engine.has_errors():
            return None

        # Attach properties for ConstantPass and HIRBuilder to use
        # In newer context-based approach, type_registry.resolved_types holds these
        self.scope_pass.node_scopes = self.context.node_scopes
        self.scope_pass.node_types = self.context.type_registry.resolved_types
        self.scope_pass.global_scope = self.context.project_scope.global_scope if self.context.project_scope else None

        # 4. Constant Pass (returns new AST)
        self.constant_pass = ConstantPass(self.diag_engine, self.scope_pass)
        folded_ast = self.constant_pass.run(ast)
        if self.diag_engine.has_errors():
            return None

        # 5. HIR Generation
        builder = HIRBuilder(self.context)
        hir = builder.build(folded_ast)
        
        # 6. HIR Validation
        from aayu.compiler.hir.validator import HIRValidator
        validator = HIRValidator(self.context)
        validator.validate(hir)
        
        return hir
