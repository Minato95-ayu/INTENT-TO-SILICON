from typing import Optional, List
from aayu.compiler.ast.nodes import (
    ProgramNode, StateDeclarationNode, LiteralNode,
    AssignmentNode, ActionDeclarationNode, ActionCallNode, IdentifierNode,
    IfNode, WhileNode, ForNode, BinaryOpNode, UnaryOpNode, EnumDeclarationNode, SubscriptNode,
    StructDeclNode, StructInitNode, ReturnNode, EnumAccessNode
)
from aayu.compiler.semantic.context import SemanticContext, TypeID
from aayu.compiler.semantic.symbols import SymbolTable
from aayu.compiler.errors import InternalCompilerError
from aayu.compiler.hir.nodes import (
    HIRModule, HIRActionDecl, HIRFunctionDecl, HIRAssignment, HIRIf, HIRLoop, HIRBlock,
    HIRVariable, HIRLiteral, HIRNullLiteral, HIRBinaryOp, HIRUnaryOp, HIRCall, HIRReturn,
    HIREnumValue, HIREnumFieldAccess, HIRStructInit, HIRStructFieldAccess,
    HIRBreak, HIRContinue, HIRNode, HIRExpr
)
from aayu.compiler.semantic.types import StructType, EnumType

class HIRBuilder:
    """
    Phase HIR-3 Builder
    Translates a verified AST into an immutable, parser-independent High-Level IR.
    Strictly follows Constitution Rule 18: No Hidden Magic. No machine details.
    Uses stable SemanticContext IDs (TypeID, SymbolID, FieldID, VariantID).
    """
    def __init__(self, context: SemanticContext):
        self.context = context
        self.type_registry = context.type_registry
        self.node_scopes = context.node_scopes
        self.global_scope = context.project_scope.global_scope if context.project_scope else None

    def build(self, ast: ProgramNode) -> HIRModule:
        self.module_id = getattr(ast, 'module_id', 'local')
        globals_list = []
        actions = []
        functions = []
        
        for stmt in ast.statements:
            if isinstance(stmt, StateDeclarationNode):
                val = self._build_expr(stmt.value, self.global_scope)
                target = HIRVariable(
                    origin_node_id=stmt.node_id, 
                    type_id=val.type_id,
                    name=stmt.name,
                    symbol_id=self.context.symbol_registry.get_symbol_id(self.module_id, stmt.name),
                    is_global=True
                )
                globals_list.append(HIRAssignment(
                    origin_node_id=stmt.node_id,
                    target=target,
                    value=val
                ))
            elif isinstance(stmt, ActionDeclarationNode):
                actions.append(self._build_action(stmt))
                
        # Struct and Enum declarations are NO LONGER emitted to HIR.
        # They live purely in the SemanticContext (TypeRegistry).
        
        return HIRModule(
            origin_node_id=ast.node_id,
            globals=globals_list, 
            actions=actions,
            functions=functions
        )

    def _get_type_id(self, node_id: int) -> TypeID:
        t = self.type_registry.resolved_types.get(node_id)
        if not t:
            raise InternalCompilerError(
                phase="HIR Generation",
                invariant="Type missing in SemanticContext (No Fallback)",
                node_id=node_id,
                module=getattr(self, 'module_id', '<unknown>')
            )
        
        # If the type itself doesn't have an ID assigned directly, 
        # it should have been registered. For primitive, struct, enum:
        if hasattr(t, 'name'):
            # In a real compiler, we would ensure ALL types have a TypeID
            # For this MVP, we map back to the TypeID via the registry
            if isinstance(t, StructType) or isinstance(t, EnumType):
                # We need the qualified name, assuming scope::name 
                # This depends on how it was registered. Let's do a reverse lookup.
                for qid, t_obj in self.type_registry.registered_types.items():
                    if t_obj is t:
                        tid = self.type_registry.get_id(qid)
                        if tid is None:
                            raise InternalCompilerError(
                                phase="HIR Generation",
                                invariant=f"Type {qid} not registered with ID",
                                node_id=node_id,
                                module=getattr(self, 'module_id', '<unknown>')
                            )
                        return tid
            else:
                # Primitive
                tid = self.type_registry.get_id(f"core::{t.name}")
                if tid is None:
                    raise InternalCompilerError(
                        phase="HIR Generation",
                        invariant=f"Primitive type core::{t.name} not registered with ID",
                        node_id=node_id,
                        module=getattr(self, 'module_id', '<unknown>')
                    )
                return tid
                
        raise InternalCompilerError(
            phase="HIR Generation",
            invariant="Could not resolve TypeID for type object",
            node_id=node_id,
            module=getattr(self, 'module_id', '<unknown>')
        )

    def _build_action(self, node: ActionDeclarationNode) -> HIRActionDecl:
        scope = self.node_scopes.get(id(node), self.global_scope)
        body_stmts = []
        for stmt in getattr(node, 'statements', []):
            built_stmt = self._build_stmt(stmt, scope)
            if built_stmt:
                body_stmts.append(built_stmt)
                
        body_block = HIRBlock(
            origin_node_id=node.node_id,
            statements=body_stmts
        )
        return HIRActionDecl(
            origin_node_id=node.node_id,
            name=node.name,
            symbol_id=self.context.symbol_registry.get_symbol_id(self.module_id, node.name),
            body=body_block,
            effect="StateMutation"
        )

    def _build_stmt(self, node, scope: SymbolTable) -> Optional[HIRNode]:
        if isinstance(node, AssignmentNode):
            val = self._build_expr(node.value, scope)
            target_expr = self._build_expr(node.target, scope)
            
            return HIRAssignment(
                origin_node_id=node.node_id,
                target=target_expr, 
                value=val
            )
            
        elif isinstance(node, IfNode):
            cond = self._build_expr(node.condition, scope)
            
            then_stmts = [self._build_stmt(s, scope) for s in node.then_branch]
            then_block = HIRBlock(
                origin_node_id=node.node_id, 
                statements=[s for s in then_stmts if s is not None]
            )
            
            else_block = None
            if node.else_branch is not None:
                else_stmts = [self._build_stmt(s, scope) for s in node.else_branch]
                else_block = HIRBlock(
                    origin_node_id=node.node_id,
                    statements=[s for s in else_stmts if s is not None]
                )
                
            return HIRIf(
                origin_node_id=node.node_id,
                condition=cond, 
                then_branch=then_block, 
                else_branch=else_block
            )
            
        elif isinstance(node, WhileNode):
            loop_scope = self.node_scopes.get(id(node), scope)
            cond = self._build_expr(node.condition, loop_scope)
            
            body_stmts = [self._build_stmt(s, loop_scope) for s in node.body]
            body_block = HIRBlock(
                origin_node_id=node.node_id,
                statements=[s for s in body_stmts if s is not None]
            )
            
            return HIRLoop(
                origin_node_id=node.node_id,
                condition=cond, 
                body=body_block
            )
            
        elif isinstance(node, ActionCallNode):
            return self._build_expr(node, scope)
            
        elif isinstance(node, StateDeclarationNode):
            val = self._build_expr(node.value, scope)
            qsym = self.context.symbol_registry.resolved_symbols.get(node.node_id)
            if qsym:
                sym_id = qsym.symbol_id
            else:
                sym_id = self.context.symbol_registry.get_symbol_id(self.module_id, node.name)
                
            target = HIRVariable(
                origin_node_id=node.node_id,
                type_id=val.type_id,
                name=node.name,
                symbol_id=sym_id,
                is_global=True
            )
            return HIRAssignment(
                origin_node_id=node.node_id,
                target=target, 
                value=val
            )
            
        elif isinstance(node, ReturnNode):
            val = self._build_expr(node.value, scope) if node.value else None
            return HIRReturn(
                origin_node_id=node.node_id,
                value=val
            )
            
        elif type(node).__name__ == "BreakNode":
            return HIRBreak(origin_node_id=node.node_id)
            
        elif type(node).__name__ == "ContinueNode":
            return HIRContinue(origin_node_id=node.node_id)
            
        return None

    def _build_expr(self, node, scope: SymbolTable) -> HIRExpr:
        t_id = self._get_type_id(node.node_id)
        
        if isinstance(node, LiteralNode):
            if node.value is None:
                return HIRNullLiteral(origin_node_id=node.node_id, type_id=t_id)
            return HIRLiteral(
                origin_node_id=node.node_id,
                value=node.value, 
                type_id=t_id
            )
            
        elif isinstance(node, IdentifierNode):
            sym = scope.resolve(node.name)
            is_global = (sym.symbol_type == 'state') if sym else False
            
            qsym = self.context.symbol_registry.resolved_symbols.get(node.node_id)
            if qsym:
                sym_id = qsym.symbol_id
            else:
                sym_id = self.context.symbol_registry.get_symbol_id(self.module_id, node.name)
                
            return HIRVariable(
                origin_node_id=node.node_id,
                name=node.name,
                symbol_id=sym_id,
                is_global=is_global,
                type_id=t_id
            )
            
        elif isinstance(node, BinaryOpNode):
            left = self._build_expr(node.left, scope)
            right = self._build_expr(node.right, scope)
            return HIRBinaryOp(
                origin_node_id=node.node_id,
                operator=node.operator, 
                left=left, 
                right=right, 
                type_id=t_id
            )

        elif isinstance(node, UnaryOpNode):
            operand = self._build_expr(node.right, scope)
            return HIRUnaryOp(
                origin_node_id=node.node_id,
                operator=node.operator,
                operand=operand,
                type_id=t_id
            )
            
        elif isinstance(node, ActionCallNode):
            args = [self._build_expr(arg, scope) for arg in node.args]
            
            qsym = self.context.symbol_registry.resolved_symbols.get(node.node_id)
            if qsym:
                sym_id = qsym.symbol_id
            else:
                sym_id = self.context.symbol_registry.get_symbol_id(self.module_id, node.name)
                
            return HIRCall(
                origin_node_id=node.node_id,
                target_symbol_id=sym_id,
                args=args, 
                type_id=t_id
            )
            
        elif isinstance(node, EnumAccessNode):
            qsym = scope.resolve(node.enum_name)
            if qsym and isinstance(qsym.data_type, EnumType):
                variant = qsym.data_type.variant_by_name(node.variant)
                if variant:
                    return HIREnumValue(
                        origin_node_id=node.node_id,
                        enum_type_id=t_id,
                        variant_id=variant.variant_id,
                        result_type_id=t_id,
                        type_id=t_id
                    )
            raise InternalCompilerError(
                phase="HIR Generation",
                invariant=f"Unresolved EnumAccessNode: {node.enum_name}::{node.variant}",
                node_id=node.node_id,
                module=getattr(self, 'module_id', '<unknown>')
            )
            
        elif isinstance(node, SubscriptNode):
            target_expr = self._build_expr(node.target, scope)
            target_type = self.type_registry.resolved_types.get(node.target.node_id, None)
            
            if isinstance(target_type, StructType):
                field_name = str(node.index.value)
                field = target_type.get_field(field_name)
                if field:
                    return HIRStructFieldAccess(
                        origin_node_id=node.node_id,
                        target=target_expr,
                        struct_type_id=target_expr.type_id,
                        field_id=field.field_id,
                        result_type_id=t_id,
                        type_id=t_id
                    )
                    
            raise InternalCompilerError(
                phase="HIR Generation",
                invariant="Unresolved SubscriptNode field access",
                node_id=node.node_id,
                module=getattr(self, 'module_id', '<unknown>')
            )
            
        elif isinstance(node, StructInitNode):
            struct_type = self.type_registry.resolved_types.get(node.node_id, None)
            if isinstance(struct_type, StructType):
                ordered_args = [None] * len(struct_type.fields)
                for field_name, expr in node.args.items():
                    field = struct_type.get_field(field_name)
                    if field:
                        # Find the index of the field for stable ordering
                        idx = struct_type.fields.index(field)
                        ordered_args[idx] = self._build_expr(expr, scope)
                
                for i in range(len(ordered_args)):
                    if ordered_args[i] is None:
                        raise InternalCompilerError(
                            phase="HIR Generation",
                            invariant="Missing struct field argument",
                            node_id=node.node_id,
                            module=getattr(self, 'module_id', '<unknown>')
                        )
                        
                return HIRStructInit(
                    origin_node_id=node.node_id,
                    struct_type_id=t_id, 
                    args=ordered_args, 
                    type_id=t_id
                )
            
        raise InternalCompilerError(
            phase="HIR Generation",
            invariant=f"Unhandled AST node in HIRBuilder: {type(node).__name__}",
            node_id=node.node_id,
            module=getattr(self, 'module_id', '<unknown>')
        )
