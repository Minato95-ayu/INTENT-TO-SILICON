from typing import Dict, Any, Optional
from aayu.compiler.ast.nodes import (
    ASTNode, IdentifierNode, ImportNode, ProjectNode, ProgramNode,
    ActionCallNode, StructInitNode, EnumAccessNode
)
from aayu.compiler.semantic.symbols import SymbolTable
from aayu.compiler.semantic.diagnostics import DiagnosticSeverity, Diagnostic
from aayu.compiler.semantic.scope_pass import ScopePass
from aayu.compiler.semantic.context import SemanticContext
from aayu.compiler.pass_manager import CompilerPass

class QualifiedSymbol:
    def __init__(self, module_id: str, local_name: str, symbol: Any):
        self.module_id = module_id
        self.local_name = local_name
        self.symbol = symbol
        # Stable integer hash for symbol resolution
        import hashlib
        hash_bytes = hashlib.sha256(f"{module_id}::{local_name}".encode('utf-8')).digest()
        self.symbol_id = int.from_bytes(hash_bytes[:8], byteorder='big')

class SymbolPass(CompilerPass):
    """
    Phase 12.0 Semantic Pipeline - Pass 2: Symbol Resolver
    Phase 2 (Multi-file): Implements strict Namespace Resolution and Import Validation.
    Constitution v1.0 Compliant: Immutable AST, Immutable Outputs, Deterministic Symbol IDs.
    """
    requires = [ScopePass]

    def __init__(self):
        self.context: Optional[SemanticContext] = None
        self.current_imports: Dict[str, str] = {} # prefix -> module_id

    def run_with_context(self, node: ASTNode, context: SemanticContext) -> ASTNode:
        self.context = context
        if isinstance(node, ProjectNode):
            for module_id, program_node in node.modules.items():
                self._run_module(module_id, program_node)
        elif isinstance(node, ProgramNode):
            # Single file fallback
            self._run_module("__main__", node)
            
        return node

    def run(self, node: Any) -> Any:
        raise Exception("SymbolPass requires a SemanticContext.")

    def _run_module(self, module_id: str, program_node: ProgramNode):
        self.current_imports.clear()
        
        # 1. Collect and validate imports
        for stmt in program_node.statements:
            if isinstance(stmt, ImportNode):
                mod_path = stmt.module
                # Import Validation Rule: Check if module exists in ProjectScope
                if not self.context.project_scope.get_module(mod_path):
                    self.context.diagnostic_registry.add(Diagnostic(
                        severity=DiagnosticSeverity.ERROR,
                        message=f"Cannot import '{mod_path}'. Module not found.",
                        span=stmt.span,
                        hint="Check your Aayu.toml dependencies."
                    ))
                else:
                    prefix = mod_path.split('.')[-1]
                    self.current_imports[prefix] = mod_path
                    
        # 2. Resolve symbols in this module
        mod_scope = self.context.node_scopes.get(id(program_node))
        if mod_scope:
            self._visit(program_node, mod_scope, module_id)

    def _visit(self, node: ASTNode, current_scope: SymbolTable, module_id: str):
        if not node:
            return
            
        # Update scope if node introduces one
        if id(node) in self.context.node_scopes:
            current_scope = self.context.node_scopes[id(node)]
            
        if isinstance(node, IdentifierNode):
            self._resolve_and_store(node, node.name, current_scope, module_id)
            return
            
        if isinstance(node, ActionCallNode):
            self._resolve_and_store(node, node.name, current_scope, module_id)
            # Visit args
            for arg in node.args:
                self._visit(arg, current_scope, module_id)
            return
            
        if isinstance(node, StructInitNode):
            self._resolve_and_store(node, node.struct_name, current_scope, module_id)
            for val in node.args.values():
                self._visit(val, current_scope, module_id)
            return
            
        if isinstance(node, EnumAccessNode):
            self._resolve_and_store(node, node.enum_name, current_scope, module_id)
            return

        from aayu.compiler.ast.nodes import PrimitiveTypeNode, AssignmentNode
        if isinstance(node, PrimitiveTypeNode):
            # Resolve user-defined types (structs, enums)
            if node.name not in ["Int", "Float", "String", "Bool", "Char", "Byte", "Void", "Never", "Any", "Null", "int", "float", "str", "bool", "char", "byte", "void"]:
                self._resolve_and_store(node, node.name, current_scope, module_id)
            return

        if isinstance(node, AssignmentNode):
            if isinstance(node.target, str):
                sym = current_scope.resolve(node.target)
                # Assignment logic...
            self._visit(node.value, current_scope, module_id)
            return

        # Generic traversal
        for key, value in vars(node).items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        self._visit(item, current_scope, module_id)
            elif isinstance(value, ASTNode):
                self._visit(value, current_scope, module_id)

    def _resolve_and_store(self, node: ASTNode, name: str, current_scope: SymbolTable, current_module_id: str):
        target_mod_id = current_module_id
        symbol_name = name
        
        if name in self.current_imports:
            mod_id = self.current_imports[name]
            mod = self.context.project_scope.get_module(mod_id)
            if mod:
                qsym = QualifiedSymbol(mod_id, name, mod)
                self.context.symbol_registry.resolved_symbols[node.node_id] = qsym
            return
            
        if "." in name:
            parts = name.split(".")
            prefix = parts[0]
            symbol_name = ".".join(parts[1:])
            
            if prefix in self.current_imports:
                target_mod_id = self.current_imports[prefix]
            else:
                # Might be a method call like `user.getName()`, not a module prefix.
                # In that case, we can't fully resolve it in SymbolPass (TypePass does method resolution).
                return
                
        if target_mod_id == current_module_id:
            sym = current_scope.resolve(symbol_name)
        else:
            target_mod = self.context.project_scope.get_module(target_mod_id)
            if not target_mod:
                return
            sym = target_mod.exports.resolve(symbol_name)
        
        if sym:
            qsym = QualifiedSymbol(target_mod_id, symbol_name, sym)
            self.context.symbol_registry.resolved_symbols[node.node_id] = qsym
        else:
            suggestion = self._find_closest_match(name, current_scope)
            hint = f"Did you mean '{suggestion}'?" if suggestion else ""
            self.context.diagnostic_registry.add(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                message=f"Undefined symbol '{name}'.",
                span=node.span,
                hint=hint
            ))
            
    def _find_closest_match(self, name: str, scope: SymbolTable) -> Optional[str]:
        # Implement No Guessing Rule strictly!
        # Only suggest if there's an exact match in an imported module.
        if self.context and self.context.project_scope:
            for prefix, mod_id in self.current_imports.items():
                mod = self.context.project_scope.get_module(mod_id)
                if mod and mod.exports.resolve(name):
                    return f"{prefix}.{name}"
        return None
