from typing import Optional
from aayu.compiler.ast.nodes import (
    ProgramNode, StateDeclarationNode, ActionDeclarationNode, 
    WhileNode, ForNode, ASTNode, EnumDeclarationNode
)
from aayu.compiler.semantic.symbols import SymbolTable, Symbol
from aayu.compiler.semantic.diagnostics import DiagnosticEngine, Diagnostic, DiagnosticSeverity

from aayu.compiler.pass_manager import CompilerPass
from aayu.compiler.semantic.context import SemanticContext

class ScopePass(CompilerPass):
    """
    Phase 12.0 Semantic Pipeline - Pass 1: Scope Builder
    Constitution v1.0 Compliant.
    """
    requires = []

    def __init__(self, *args, **kwargs):
        self.context: Optional[SemanticContext] = None
        self.current_scope = None
        self.loop_depth = 0
        
    def run_with_context(self, ast: ASTNode, context: SemanticContext) -> ASTNode:
        self.context = context
        from aayu.compiler.semantic.symbols import ProjectScope, ModuleSymbol
        from aayu.compiler.ast.nodes import ProjectNode, ProgramNode
        
        if isinstance(ast, ProjectNode):
            context.project_scope = ProjectScope()
            for module_id, program_node in ast.modules.items():
                mod_sym = ModuleSymbol(name=module_id.split('.')[-1], module_id=module_id)
                context.project_scope.add_module(mod_sym)
                
                self.current_scope = mod_sym.exports
                
                builtins = ["print", "ping", "dns_resolve", "tcp_connect"]
                for b in builtins:
                    self.current_scope.define(Symbol(b, "builtin"))
                    
                context.node_scopes[id(program_node)] = self.current_scope
                self._visit(program_node)
                
            context.project_scope.freeze()
            return ast
            
        elif isinstance(ast, ProgramNode):
            if not context.project_scope:
                context.project_scope = ProjectScope()
                context.project_scope.global_scope = SymbolTable()
            self.current_scope = context.project_scope.global_scope
            context.node_scopes[id(ast)] = self.current_scope
            self.module_id = getattr(ast, 'module_id', 'local')
            self._visit(ast)
            return ast
            
    def run(self, ast: ASTNode) -> ASTNode:
        raise Exception("ScopePass requires SemanticContext")

    def _visit(self, node: ASTNode):
        if not node:
            return
            
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._default_visit)
        visitor(node)

    def _default_visit(self, node: ASTNode):
        # By default, visit all children
        for key, value in vars(node).items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        self._visit(item)
            elif isinstance(value, ASTNode):
                self._visit(value)

    def _visit_StateDeclarationNode(self, node: StateDeclarationNode):
        # Define in current scope (global)
        sym = Symbol(node.name, "state")
        if node.name in self.current_scope.symbols:
            self.context.diagnostic_registry.add(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E101",
                message=f"State '{node.name}' is already defined in this scope.",
                line=node.line, column=node.column,
                notes=[f"State variables must be unique."]
            ))
        else:
            self.current_scope.define(sym)
            
        self._visit(node.value)

    def _visit_ActionDeclarationNode(self, node: ActionDeclarationNode):
        sym = Symbol(node.name, "action")
        if node.name in self.current_scope.symbols:
            self.context.diagnostic_registry.add(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E102",
                message=f"Action '{node.name}' is already defined in this scope.",
                line=node.line, column=node.column
            ))
        else:
            self.current_scope.define(sym)

        # Create new scope for action body
        prev_scope = self.current_scope
        action_scope = SymbolTable(parent=prev_scope)
        self.current_scope = action_scope
        self.context.node_scopes[id(node)] = action_scope

        # Define arguments in local scope
        for arg in getattr(node, 'args', []):
            arg_sym = Symbol(arg, "local")
            self.current_scope.define(arg_sym)

        for stmt in node.statements:
            self._visit(stmt)

        self.current_scope = prev_scope

    def _visit_WhileNode(self, node: WhileNode):
        self._visit(node.condition)
        
        # While loops get their own scope
        prev_scope = self.current_scope
        loop_scope = SymbolTable(parent=prev_scope)
        self.current_scope = loop_scope
        self.context.node_scopes[id(node)] = loop_scope
        
        self.loop_depth += 1
        for stmt in node.body:
            self._visit(stmt)
        self.loop_depth -= 1
            
        self.current_scope = prev_scope

    def _visit_ForNode(self, node: ForNode):
        self._visit(node.iterable)
        
        prev_scope = self.current_scope
        loop_scope = SymbolTable(parent=prev_scope)
        self.current_scope = loop_scope
        self.context.node_scopes[id(node)] = loop_scope
        
        # Define iterator
        self.current_scope.define(Symbol(node.iterator, "local"))
        if getattr(node, 'index_name', None):
            self.current_scope.define(Symbol(node.index_name, "local"))
            
        self.loop_depth += 1
        for stmt in node.body:
            self._visit(stmt)
        self.loop_depth -= 1
            
        self.current_scope = prev_scope

    def _visit_BreakNode(self, node):
        if self.loop_depth == 0:
            self.context.diagnostic_registry.add(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E105",
                message="'break' can only be used inside a loop.",
                line=node.line, column=node.column
            ))

    def _visit_ContinueNode(self, node):
        if self.loop_depth == 0:
            self.context.diagnostic_registry.add(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E106",
                message="'continue' can only be used inside a loop.",
                line=node.line, column=node.column
            ))

    def _visit_AssignmentNode(self, node):
        from aayu.compiler.ast.nodes import IdentifierNode
        target_name = node.target.name if isinstance(node.target, IdentifierNode) else str(node.target)
        if not self.current_scope.resolve(target_name):
            sym = Symbol(target_name, "local")
            self.current_scope.define(sym)
        self._visit(node.value)

    def _visit_EnumDeclarationNode(self, node: EnumDeclarationNode):
        """
        Register enum as a type symbol in the current scope.
        Each variant is registered as a constant symbol under the enum's namespace.
        The EnumType and EnumVariant objects are constructed here so the TypePass
        can simply look them up instead of rebuilding them.
        """
        from aayu.compiler.semantic.types import EnumType, EnumVariant

        # Build the semantic EnumType with auto-tagged variants
        variants = []
        enum_qualified_name = f"{self.module_id}::{node.name}"
        for i, variant_name in enumerate(node.variants):
            v = EnumVariant(name=variant_name, tag=i)
            v.generate_id(enum_qualified_name)
            variants.append(v)

        enum_type = EnumType(name=node.name, variants=variants)

        # Register the enum name as a type symbol
        enum_sym = Symbol(node.name, "enum")
        enum_sym.data_type = enum_type
        enum_sym.is_mutable = False

        if node.name in self.current_scope.symbols:
            self.context.diagnostic_registry.add(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E103",
                message=f"Enum '{node.name}' is already defined in this scope.",
                line=node.line, column=node.column
            ))
        else:
            self.current_scope.define(enum_sym)

        # Register each variant as a constant in the current scope
        # Accessible as Color.Red via SubscriptNode/EnumAccessNode resolution
        for variant in variants:
            variant_sym = Symbol(f"{node.name}.{variant.name}", "enum_variant")
            variant_sym.data_type = enum_type
            variant_sym.is_mutable = False
            variant_sym.is_constant = True
            self.current_scope.define(variant_sym)

    def _visit_StructDeclNode(self, node):
        from aayu.compiler.semantic.types import StructType, StructField
        
        # Build semantic StructType
        fields = []
        struct_qualified_name = f"{self.module_id}::{node.name}"
        for i, field_node in enumerate(node.fields):
            # field_type resolution is done in TypePass, here we just stub the structure
            from aayu.compiler.semantic.types import T_ANY
            f = StructField(name=field_node.name, field_type=T_ANY, index=i)
            f.generate_id(struct_qualified_name)
            fields.append(f)
            
        struct_type = StructType(name=node.name, fields=fields, field_count=len(fields))
        
        struct_sym = Symbol(node.name, "struct")
        struct_sym.data_type = struct_type
        
        if node.name in self.current_scope.symbols:
            self.context.diagnostic_registry.add(Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                code="E104",
                message=f"Struct '{node.name}' is already defined in this scope.",
                line=node.line, column=node.column
            ))
        else:
            self.current_scope.define(struct_sym)
