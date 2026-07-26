from typing import List
from compiler.semantic.nodes import (
    SemanticProgramNode, SemanticStateDeclNode, SemanticWidgetNode,
    SemanticLiteralNode, SemanticAssignmentNode, SemanticImportNode,
    SemanticActionDeclNode, SemanticActionCallNode, SemanticIdentifierNode,
    SemanticIfNode, SemanticForNode, SemanticBinaryOpNode, SemanticModelDeclNode,
    SemanticRouteNode, SemanticReturnNode,
    SemanticThemeNode, SemanticNavigateNode, SemanticPropDeclNode,
    SemanticUseThemeNode, SemanticDictionaryNode, SemanticAwaitNode, SemanticBindNode, SemanticValidateNode,
    SemanticValidateFieldNode, SemanticValidationRuleNode, SemanticAnimateNode,
    SemanticLifecycleNode, SemanticArrayNode, SemanticSubscriptNode,
    SemanticTryNode, SemanticThrowNode, SemanticRethrowNode
)
from compiler.ir.hir import (
    HIRNode, HIRStateDecl, HIRWidget, HIRAssignment,
    HIRActionDecl, HIRActionCall, HIRLoadVar, HIRPrint, HIRImport,
    HIRIf, HIRFor, HIRBinaryOp, HIRLoadConst,
    HIRModel, HIRModelField, HIRModelAttribute, HIRRoute, HIRMethod, HIRReturn,
    HIRTheme, HIRNavigate, HIRUseTheme, HIRDictionary, HIRAwait, HIRBind, HIRValidate, HIRAnimate, HIRLifecycle,
    HIRArrayNode, HIRSubscript,
    HIRTry, HIRThrow, HIRRethrow
)
from compiler.ir.mir import MIRNode, MIRInstruction
from compiler.ir.lir import LIRNode

class IRPipeline:
    """Three-stage IR lowering: Semantic AST → HIR → MIR → LIR"""

    # ── HIR Stage ──────────────────────────────────────────────

    def to_hir(self, semantic_ast: SemanticProgramNode) -> List[HIRNode]:
        hir_list = []
        for stmt in semantic_ast.statements:
            hir_node = self._semantic_to_hir(stmt)
            if hir_node is not None:
                hir_list.append(hir_node)
        return hir_list

    def _semantic_to_hir(self, node):
        if isinstance(node, SemanticStateDeclNode):
            val_hir = self._semantic_to_hir(node.value)
            if isinstance(val_hir, HIRPrint): val_hir = HIRLoadConst(val_hir.value)
            return HIRStateDecl(node.name, val_hir)

        elif isinstance(node, SemanticWidgetNode):
            children_hir = []
            for child in node.children:
                child_hir = self._semantic_to_hir(child)
                if child_hir is not None:
                    children_hir.append(child_hir)
            props_hir = {}
            for k, v in node.props.items():
                if hasattr(v, 'line'):  # Check if it's a SemanticNode
                    props_hir[k] = self._semantic_to_hir(v)
                else:
                    props_hir[k] = v
            return HIRWidget(node.widget_type, props_hir, children_hir)

        elif isinstance(node, SemanticAssignmentNode):
            val_hir = self._semantic_to_hir(node.value)
            if isinstance(val_hir, HIRPrint): val_hir = HIRLoadConst(val_hir.value)
            return HIRAssignment(node.target, val_hir)

        elif isinstance(node, SemanticActionDeclNode):
            body_hir = []
            for stmt in node.statements:
                h = self._semantic_to_hir(stmt)
                if h is not None:
                    body_hir.append(h)
            decorators = [{"name": d.name, "args": d.args} for d in getattr(node, "decorators", [])]
            return HIRActionDecl(node.name, body_hir, node.args, decorators)

        elif isinstance(node, SemanticActionCallNode):
            arg_hirs = []
            for a in getattr(node, 'args', []):
                h = self._semantic_to_hir(a)
                if isinstance(h, HIRPrint):
                    h = HIRLoadConst(h.value)
                arg_hirs.append(h)
            return HIRActionCall(node.name, arg_hirs)

        elif isinstance(node, SemanticIdentifierNode):
            return HIRLoadVar(node.name)

        elif isinstance(node, SemanticArrayNode):
            elements_hir = []
            for el in node.elements:
                h = self._semantic_to_hir(el)
                if isinstance(h, HIRPrint):
                    h = HIRLoadConst(h.value)
                elements_hir.append(h)
            from compiler.ir.hir import HIRArrayNode
            return HIRArrayNode(elements=elements_hir)

        elif isinstance(node, SemanticImportNode):
            return HIRImport(node.module)

        elif isinstance(node, SemanticBinaryOpNode):
            left_hir = self._semantic_to_hir(node.left)
            right_hir = self._semantic_to_hir(node.right)
            if isinstance(left_hir, HIRPrint): left_hir = HIRLoadConst(left_hir.value)
            if isinstance(right_hir, HIRPrint): right_hir = HIRLoadConst(right_hir.value)
            return HIRBinaryOp(left_hir, node.op, right_hir)

        elif isinstance(node, SemanticIfNode):
            cond_hir = self._semantic_to_hir(node.condition)
            if isinstance(cond_hir, HIRPrint): cond_hir = HIRLoadConst(cond_hir.value)
            then_hir = []
            for stmt in node.then_branch:
                h = self._semantic_to_hir(stmt)
                if h is not None: then_hir.append(h)
            else_hir = []
            if node.else_branch is not None:
                for stmt in node.else_branch:
                    h = self._semantic_to_hir(stmt)
                    if h is not None: else_hir.append(h)
            return HIRIf(cond_hir, then_hir, else_hir)

        elif isinstance(node, SemanticForNode):
            iter_hir = self._semantic_to_hir(node.iterable)
            if isinstance(iter_hir, HIRPrint): iter_hir = HIRLoadConst(iter_hir.value)
            
            body_hir = []
            for stmt in node.body:
                h = self._semantic_to_hir(stmt)
                if h is not None: body_hir.append(h)
                
            return HIRFor(node.iterator, iter_hir, body_hir, index_name=node.index_name)

        elif isinstance(node, SemanticModelDeclNode):
            fields = []
            for f in node.fields:
                attrs = [HIRModelAttribute(a.name, a.args) for a in f.attributes]
                fields.append(HIRModelField(f.name, f.field_type, attrs))
            return HIRModel(node.name, fields, decorators=node.decorators)
            
        elif isinstance(node, SemanticReturnNode):
            val_hir = self._semantic_to_hir(node.value)
            return HIRReturn(val_hir)

        elif isinstance(node, SemanticTryNode):
            try_hir = [self._semantic_to_hir(s) for s in node.try_block if self._semantic_to_hir(s) is not None]
            catch_hir = [self._semantic_to_hir(s) for s in node.catch_block if self._semantic_to_hir(s) is not None]
            finally_hir = [self._semantic_to_hir(s) for s in node.finally_block if self._semantic_to_hir(s) is not None]
            return HIRTry(try_hir, node.catch_var, catch_hir, finally_hir)

        elif isinstance(node, SemanticThrowNode):
            val_hir = self._semantic_to_hir(node.value)
            return HIRThrow(val_hir)

        elif isinstance(node, SemanticRethrowNode):
            return HIRRethrow()

        elif isinstance(node, SemanticRouteNode):
            methods = []
            for m in node.methods:
                body_hir = []
                for stmt in m.body:
                    h = self._semantic_to_hir(stmt)
                    if h is not None: body_hir.append(h)
                methods.append(HIRMethod(m.method, body_hir))
            return HIRRoute(node.path, methods)
            
        elif isinstance(node, SemanticReturnNode):
            val_hir = self._semantic_to_hir(node.value)
            if isinstance(val_hir, HIRPrint): val_hir = HIRLoadConst(val_hir.value)
            return HIRReturn(val_hir)
        elif isinstance(node, SemanticLiteralNode):
            # Standalone literal (e.g. inside a widget child list)
            return HIRPrint(node.value)

        elif isinstance(node, SemanticThemeNode):
            return HIRTheme(node.name, node.properties)
        
        elif isinstance(node, SemanticUseThemeNode):
            return HIRUseTheme(node.name)

        elif isinstance(node, SemanticNavigateNode):
            kwargs_hir = {}
            for k, v in node.kwargs.items():
                hir_v = self._semantic_to_hir(v)
                if hir_v is not None:
                    kwargs_hir[k] = hir_v
            return HIRNavigate(node.target, kwargs_hir)

        elif isinstance(node, SemanticPropDeclNode):
            # Props are handled implicitly by the interpreter scope injection
            return None

        elif isinstance(node, SemanticDictionaryNode):
            pairs = {}
            for k, v in node.pairs.items():
                v_hir = self._semantic_to_hir(v)
                if isinstance(v_hir, HIRPrint): v_hir = HIRLoadConst(v_hir.value)
                pairs[k] = v_hir
            return HIRDictionary(pairs)
            
        elif isinstance(node, SemanticSubscriptNode):
            target_hir = self._semantic_to_hir(node.target)
            if isinstance(target_hir, HIRPrint): target_hir = HIRLoadConst(target_hir.value)
            index_hir = self._semantic_to_hir(node.index)
            if isinstance(index_hir, HIRPrint): index_hir = HIRLoadConst(index_hir.value)
            return HIRSubscript(target_hir, index_hir)

        elif isinstance(node, SemanticAwaitNode):
            expr_hir = self._semantic_to_hir(node.expression)
            return HIRAwait(expr_hir)
            
        elif isinstance(node, SemanticBindNode):
            return HIRBind(node.target)
            
        elif isinstance(node, SemanticValidateNode):
            # Pass fields down directly for MIR translation
            return HIRValidate(node.fields)
            
        elif isinstance(node, SemanticAnimateNode):
            props_hir = {}
            for k, v in node.properties.items():
                v_hir = self._semantic_to_hir(v)
                if isinstance(v_hir, HIRPrint): v_hir = HIRLoadConst(v_hir.value)
                props_hir[k] = v_hir
            return HIRAnimate(props_hir)
            
        elif isinstance(node, SemanticLifecycleNode):
            body_hir = []
            for stmt in node.body:
                h = self._semantic_to_hir(stmt)
                if h is not None: body_hir.append(h)
            return HIRLifecycle(node.hook, body_hir)

        elif type(node).__name__ == "SemanticClosureNode":
            arg_hirs = []
            for a in node.args:
                h = self._semantic_to_hir(a)
                if isinstance(h, HIRPrint): h = HIRLoadConst(h.value)
                arg_hirs.append(h)
            from compiler.ir.hir import HIRClosure
            return HIRClosure(node.action_name, arg_hirs)

        return None

    # ── MIR Stage ──────────────────────────────────────────────

    def to_mir(self, hir_list: List[HIRNode]) -> List[MIRNode]:
        mir_list = []
        for hir in hir_list:
            self._hir_to_mir(hir, mir_list)
        return mir_list

    def _hir_to_mir(self, hir, mir_list: list):
        if isinstance(hir, HIRStateDecl):
            self._hir_to_mir(hir.value, mir_list)
            mir_list.append(MIRInstruction("INIT_STATE", [hir.name]))

        elif isinstance(hir, HIRWidget):
            if hir.w_type.lower() in ["text", "heading", "button"]:
                # First recursively process children
                for child in hir.children:
                    self._hir_to_mir(child, mir_list)
                
                props = hir.props.copy() if isinstance(hir.props, dict) else {"value": hir.props}
                for k, v in list(props.items()):
                    if isinstance(v, HIRPrint):
                        # HIRPrint as prop value: push value on stack, don't print
                        mir_list.append(MIRInstruction("PUSH_CONST", [v.value]))
                        props[k] = "$STACK"
                    elif hasattr(v, 'opcode') or type(v).__name__.startswith("HIR"):
                        self._hir_to_mir(v, mir_list)
                        props[k] = "$STACK"
                    elif type(v).__name__ == "SemanticIdentifierNode":
                        mir_list.append(MIRInstruction("LOAD_VAR", [v.name]))
                        props[k] = "$STACK"
                    elif type(v).__name__ == "IdentifierNode":
                        mir_list.append(MIRInstruction("LOAD_VAR", [v.name]))
                        props[k] = "$STACK"
                
                mir_list.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [props]))
                return
            if hir.w_type.lower() in ["page", "component"]:
                page_name = hir.props.get("name", "")
                
                if hir.w_type.lower() == "page":
                    body_mir = []
                    body_mir.append(MIRInstruction("MARK_BLOCK_START", []))
                    for child in hir.children:
                        self._hir_to_mir(child, body_mir)
                    body_mir.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [hir.props]))
                    mir_list.append(MIRInstruction("ACTION_DECL", [f"__PAGE_START_{page_name}", body_mir]))
                    # For legacy compatibility, also map the first page to __PAGE_START__
                    if not getattr(self, '_first_page_seen', False):
                        mir_list.append(MIRInstruction("ACTION_DECL", ["__PAGE_START__", body_mir]))
                        self._first_page_seen = True
                else:
                    # Components are compiled as actions!
                    body_mir = []
                    body_mir.append(MIRInstruction("MARK_BLOCK_START", []))
                    for child in hir.children:
                        self._hir_to_mir(child, body_mir)
                    body_mir.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [hir.props]))
                    mir_list.append(MIRInstruction("ACTION_DECL", [page_name, body_mir]))
            elif hir.w_type.lower() == "call":
                # calling a component is calling its action
                target = hir.props.get("target", "")
                if not target and hir.children:
                    # In parser, `call Navbar` puts Identifier("Navbar") as a child
                    first_child = hir.children[0]
                    if hasattr(first_child, "name"):
                        target = first_child.name
                mir_list.append(MIRInstruction("CALL_ACTION", [target]))
            else:
                is_block = hir.w_type.lower() in [
                    "container", "row", "column", "card", "stack", "center",
                    "expanded", "padding", "scrollview", "grid",
                    "appbar", "navigationbar", "list", "form", "dialog",
                    "drawer", "snackbar", "tabbar", "scaffold"
                ]
                if is_block:
                    mir_list.append(MIRInstruction("MARK_BLOCK_START", []))
                    
                # First recursively process children
                for child in hir.children:
                    self._hir_to_mir(child, mir_list)
                # Then emit the widget itself
                props = hir.props.copy() if isinstance(hir.props, dict) else {"value": hir.props}
                for k, v in list(props.items()):
                    if isinstance(v, HIRPrint):
                        # HIRPrint as prop value: push value on stack, don't print
                        mir_list.append(MIRInstruction("PUSH_CONST", [v.value]))
                        props[k] = "$STACK"
                    elif hasattr(v, 'opcode') or type(v).__name__.startswith("HIR"):
                        self._hir_to_mir(v, mir_list)
                        props[k] = "$STACK"
                    elif type(v).__name__ == "SemanticIdentifierNode":
                        mir_list.append(MIRInstruction("LOAD_VAR", [v.name]))
                        props[k] = "$STACK"
                    elif type(v).__name__ == "IdentifierNode":
                        mir_list.append(MIRInstruction("LOAD_VAR", [v.name]))
                        props[k] = "$STACK"
                
                mir_list.append(MIRInstruction(f"INIT_{hir.w_type.upper()}", [props]))
        elif isinstance(hir, HIRAssignment):
            self._hir_to_mir(hir.value, mir_list)
            mir_list.append(MIRInstruction("SET_STATE", [hir.target]))

        elif isinstance(hir, HIRActionDecl):
            body_mir = []
            
            # Inject CHECK_AUTH if auth_required decorator is present
            if any(d.get("name") == "auth_required" for d in getattr(hir, "decorators", [])):
                body_mir.append(MIRInstruction("CHECK_AUTH", []))
                
            for stmt in hir.body:
                self._hir_to_mir(stmt, body_mir)
            mir_list.append(MIRInstruction("ACTION_DECL", [hir.name, body_mir, hir.args]))

        elif isinstance(hir, HIRActionCall):
            for arg in hir.args:
                self._hir_to_mir(arg, mir_list)
            if "." in hir.name or hir.name in ["print", "len", "type"]:
                mir_list.append(MIRInstruction("OP_ASYNC_CALL", [hir.name, len(hir.args)]))
            else:
                mir_list.append(MIRInstruction("CALL_ACTION", [hir.name]))

        elif isinstance(hir, HIRTheme):
            mir_list.append(MIRInstruction("DECLARE_THEME", [hir.name, hir.properties]))
            
        elif isinstance(hir, HIRUseTheme):
            mir_list.append(MIRInstruction("SET_THEME", [hir.name]))
            

        elif isinstance(hir, HIRLoadVar):
            mir_list.append(MIRInstruction("LOAD_VAR", [hir.name]))
            
        elif isinstance(hir, HIRLoadConst):
            mir_list.append(MIRInstruction("PUSH_CONST", [hir.value]))

        elif isinstance(hir, HIRModel):
            mir_list.append(MIRInstruction("MODEL_DECL", [hir]))

        elif isinstance(hir, HIRTry):
            import uuid
            uid = uuid.uuid4().hex[:8]
            catch_label = f"catch_{uid}"
            finally_label = f"finally_{uid}"
            end_label = f"end_try_{uid}"

            # If there's no catch block, just go straight to finally on error
            error_target = catch_label if hir.catch_block else finally_label

            mir_list.append(MIRInstruction("SETUP_EXCEPT", [error_target]))
            for stmt in hir.try_block:
                self._hir_to_mir(stmt, mir_list)
            mir_list.append(MIRInstruction("POP_EXCEPT", []))
            mir_list.append(MIRInstruction("JUMP", [finally_label]))

            if hir.catch_block:
                mir_list.append(MIRInstruction("LABEL", [catch_label]))
                if hir.catch_var:
                    # Exception object is on stack
                    mir_list.append(MIRInstruction("SET_STATE", [hir.catch_var]))
                else:
                    # discard exception if not captured
                    mir_list.append(MIRInstruction("POP", []))
                    
                for stmt in hir.catch_block:
                    self._hir_to_mir(stmt, mir_list)
                
                mir_list.append(MIRInstruction("JUMP", [finally_label]))

            mir_list.append(MIRInstruction("LABEL", [finally_label]))
            for stmt in hir.finally_block:
                self._hir_to_mir(stmt, mir_list)

        elif isinstance(hir, HIRThrow):
            self._hir_to_mir(hir.value, mir_list)
            mir_list.append(MIRInstruction("THROW", []))

        elif isinstance(hir, HIRRethrow):
            mir_list.append(MIRInstruction("RETHROW", []))

        elif isinstance(hir, HIRPrint):
            mir_list.append(MIRInstruction("PRINT", [hir.value]))

        elif isinstance(hir, HIRImport):
            # Imports are resolved at semantic stage; skip in IR
            pass

        elif isinstance(hir, HIRBinaryOp):
            self._hir_to_mir(hir.left, mir_list)
            self._hir_to_mir(hir.right, mir_list)
            mir_list.append(MIRInstruction("BINARY_OP", [hir.op]))

        elif isinstance(hir, HIRIf):
            self._hir_to_mir(hir.condition, mir_list)
            
            import uuid
            else_label = f"else_{uuid.uuid4().hex[:8]}"
            end_label = f"end_if_{uuid.uuid4().hex[:8]}"
            
            mir_list.append(MIRInstruction("JUMP_IF_FALSE", [else_label]))
            for stmt in hir.then_branch:
                self._hir_to_mir(stmt, mir_list)
            mir_list.append(MIRInstruction("JUMP", [end_label]))
            mir_list.append(MIRInstruction("LABEL", [else_label]))
            if hir.else_branch:
                for stmt in hir.else_branch:
                    self._hir_to_mir(stmt, mir_list)
            mir_list.append(MIRInstruction("LABEL", [end_label]))

        elif isinstance(hir, HIRFor):
            import uuid
            uid = uuid.uuid4().hex[:8]
            start_label = f"for_start_{uid}"
            end_label = f"for_end_{uid}"
            idx_var = f"__idx_{uid}"
            len_var = f"__len_{uid}"
            array_var = f"__arr_{uid}"

            # Evaluate iterable and store in hidden array var
            self._hir_to_mir(hir.iterable, mir_list)
            mir_list.append(MIRInstruction("SET_STATE", [array_var]))

            # Store length
            mir_list.append(MIRInstruction("LOAD_VAR", [array_var]))
            mir_list.append(MIRInstruction("GET_LENGTH", []))
            mir_list.append(MIRInstruction("SET_STATE", [len_var]))

            # Store index = 0
            mir_list.append(MIRInstruction("PUSH_CONST", [0]))
            mir_list.append(MIRInstruction("SET_STATE", [idx_var]))

            mir_list.append(MIRInstruction("LABEL", [start_label]))

            # Loop condition: idx < len
            mir_list.append(MIRInstruction("LOAD_VAR", [idx_var]))
            mir_list.append(MIRInstruction("LOAD_VAR", [len_var]))
            mir_list.append(MIRInstruction("BINARY_OP", ["<"]))
            mir_list.append(MIRInstruction("JUMP_IF_FALSE", [end_label]))

            # Get item: iterator = array_var[idx_var]
            mir_list.append(MIRInstruction("LOAD_VAR", [array_var]))
            mir_list.append(MIRInstruction("LOAD_VAR", [idx_var]))
            mir_list.append(MIRInstruction("LOAD_SUBSCR", []))
            mir_list.append(MIRInstruction("SET_STATE", [hir.iterator]))
            
            if hir.index_name:
                mir_list.append(MIRInstruction("LOAD_VAR", [idx_var]))
                mir_list.append(MIRInstruction("SET_STATE", [hir.index_name]))

            # Body
            for stmt in hir.body:
                self._hir_to_mir(stmt, mir_list)

            # Increment index
            mir_list.append(MIRInstruction("LOAD_VAR", [idx_var]))
            mir_list.append(MIRInstruction("PUSH_CONST", [1]))
            mir_list.append(MIRInstruction("BINARY_OP", ["+"]))
            mir_list.append(MIRInstruction("SET_STATE", [idx_var]))

            mir_list.append(MIRInstruction("JUMP", [start_label]))
            mir_list.append(MIRInstruction("LABEL", [end_label]))

        elif type(hir).__name__ == "HIRArrayNode":
            for el in hir.elements:
                self._hir_to_mir(el, mir_list)
            mir_list.append(MIRInstruction("CREATE_ARRAY", [len(hir.elements)]))

        elif isinstance(hir, HIRModel):
            fields_data = [{"name": f.name, "type": f.field_type, "attributes": [{"name": a.name, "args": a.args} for a in f.attributes]} for f in hir.fields]
            mir_list.append(MIRInstruction("CREATE_MODEL", [hir.name, fields_data, hir.decorators]))

        elif isinstance(hir, HIRRoute):
            methods_mir = []
            for m in hir.methods:
                body_mir = []
                for stmt in m.body:
                    self._hir_to_mir(stmt, body_mir)
                methods_mir.append({"method": m.method, "body": body_mir})
            mir_list.append(MIRInstruction("REGISTER_ROUTE", [hir.path, methods_mir]))

        elif isinstance(hir, HIRReturn):
            self._hir_to_mir(hir.value, mir_list)
            mir_list.append(MIRInstruction("RETURN_VALUE", []))

        elif isinstance(hir, HIRNavigate):
            num_args = len(hir.kwargs)
            keys = []
            for k, v in hir.kwargs.items():
                self._hir_to_mir(v, mir_list)
                keys.append(k)
            mir_list.append(MIRInstruction("NAVIGATE", [hir.target, keys]))

        elif isinstance(hir, HIRDictionary):
            keys = []
            for k, v in hir.pairs.items():
                self._hir_to_mir(v, mir_list)
                keys.append(k)
            mir_list.append(MIRInstruction("BUILD_DICT", [keys]))

        elif isinstance(hir, HIRSubscript):
            self._hir_to_mir(hir.target, mir_list)
            self._hir_to_mir(hir.index, mir_list)
            mir_list.append(MIRInstruction("LOAD_SUBSCR", []))
            
        elif isinstance(hir, HIRAwait):
            self._hir_to_mir(hir.expression, mir_list)
            mir_list.append(MIRInstruction("ASYNC_CALL", []))
            
        elif isinstance(hir, HIRBind):
            mir_list.append(MIRInstruction("SET_BINDING", [hir.target]))
            
        elif isinstance(hir, HIRValidate):
            val_dict = {}
            for field in hir.fields:
                rules = []
                for rule in field.rules:
                    # rule.args are semantic AST nodes, we can just extract values if they are literals
                    # For simplicity, we just keep rule.rule as string, args as list of values if any
                    args_vals = []
                    for a in rule.args:
                        from compiler.semantic.nodes import SemanticLiteralNode
                        if isinstance(a, SemanticLiteralNode):
                            args_vals.append(a.value)
                        else:
                            args_vals.append(str(a))
                    rules.append({"rule": rule.rule, "args": args_vals})
                val_dict[field.field_name] = rules
            mir_list.append(MIRInstruction("DECLARE_VALIDATION", [val_dict]))
            
        elif isinstance(hir, HIRAnimate):
            # Evaluate all properties and push them, then build the animate block
            keys = []
            for k, v in hir.properties.items():
                self._hir_to_mir(v, mir_list)
                keys.append(k)
            mir_list.append(MIRInstruction("SET_ANIMATION", [keys]))
            
        elif type(hir).__name__ == "HIRClosure":
            # push all args, then CREATE_CLOSURE
            for arg in hir.args:
                self._hir_to_mir(arg, mir_list)
            mir_list.append(MIRInstruction("CREATE_CLOSURE", [hir.action_name, len(hir.args)]))

        elif isinstance(hir, HIRLifecycle):
            body_mir = []
            for stmt in hir.body:
                self._hir_to_mir(stmt, body_mir)
            mir_list.append(MIRInstruction("DECLARE_LIFECYCLE", [hir.hook, body_mir]))

    # ── LIR Stage ──────────────────────────────────────────────

    def to_lir(self, mir_list: List[MIRNode]) -> List[LIRNode]:
        lir_list = []
        for mir in mir_list:
            self._mir_to_lir(mir, lir_list)
        return lir_list

    def _mir_to_lir(self, mir, lir_list: list):
        if not isinstance(mir, MIRInstruction):
            return

        if mir.opcode == "INIT_STATE":
            # INIT_STATE [name] → STATE_INIT [name]
            lir_list.append(LIRNode("STATE_INIT", [mir.operands[0]]))

        elif mir.opcode == "SET_STATE":
            # Value is already on stack from evaluating the expression
            lir_list.append(LIRNode("STORE_VAR", [mir.operands[0]]))

        elif mir.opcode == "MARK_PAGE_START":
            lir_list.append(LIRNode("MARK_PAGE_START", []))

        elif mir.opcode == "MARK_BLOCK_START":
            lir_list.append(LIRNode("MARK_BLOCK_START", []))

        elif mir.opcode.startswith("INIT_"):
            # INIT_TEXT, INIT_BUTTON, etc. → BUILD_*
            widget_type = mir.opcode[5:]  # strip "INIT_"
            lir_list.append(LIRNode(f"BUILD_{widget_type}", [mir.operands[0] if mir.operands else {}]))

        elif mir.opcode == "ACTION_DECL":
            # ACTION_DECL [name, body_mir_list, args]
            body_lir = []
            if len(mir.operands) > 1 and isinstance(mir.operands[1], list):
                for sub_mir in mir.operands[1]:
                    self._mir_to_lir(sub_mir, body_lir)
            args = mir.operands[2] if len(mir.operands) > 2 else []
            lir_list.append(LIRNode("ACTION_DECL", [mir.operands[0], body_lir, args]))

        elif mir.opcode == "CALL_ACTION":
            lir_list.append(LIRNode("CALL_ACTION", [mir.operands[0]]))

        elif mir.opcode == "LOAD_VAR":
            lir_list.append(LIRNode("LOAD_VAR", [mir.operands[0]]))

        elif mir.opcode == "PRINT":
            lir_list.append(LIRNode("PRINT", [mir.operands[0]]))

        elif mir.opcode == "PRINT_STACK":
            # Value is already on the stack from a preceding LOAD_VAR
            lir_list.append(LIRNode("PRINT_STACK", []))
            
        elif mir.opcode == "PUSH_CONST":
            lir_list.append(LIRNode("PUSH_CONST", [mir.operands[0]]))
            
        elif mir.opcode == "BINARY_OP":
            lir_list.append(LIRNode("BINARY_OP", [mir.operands[0]]))
            
        elif mir.opcode in ["JUMP", "JUMP_IF_FALSE", "LABEL", "GET_ITER", "FOR_ITER", "GET_LENGTH", "LOAD_SUBSCR", "STORE_SUBSCR", "CREATE_CLOSURE", "SETUP_EXCEPT", "POP_EXCEPT", "THROW", "RETHROW"]:
            lir_list.append(LIRNode(mir.opcode, mir.operands))

        elif mir.opcode == "CREATE_ARRAY":
            lir_list.append(LIRNode("CREATE_ARRAY", [mir.operands[0]]))

        elif mir.opcode == "CREATE_MODEL":
            lir_list.append(LIRNode("CREATE_MODEL", mir.operands))
            
        elif mir.opcode == "CHECK_AUTH":
            lir_list.append(LIRNode("CHECK_AUTH", []))

        elif mir.opcode == "REGISTER_ROUTE":
            # For route, we also need to convert body of each method to LIR
            methods_lir = []
            for method_data in mir.operands[1]:
                body_lir = []
                for sub_mir in method_data["body"]:
                    self._mir_to_lir(sub_mir, body_lir)
                methods_lir.append({"method": method_data["method"], "body": body_lir})
            lir_list.append(LIRNode("REGISTER_ROUTE", [mir.operands[0], methods_lir]))

        elif mir.opcode == "RETURN_VALUE":
            lir_list.append(LIRNode("RETURN_VALUE", []))

        elif mir.opcode == "SET_THEME":
            lir_list.append(LIRNode("SET_THEME", [mir.operands[0]]))

        elif mir.opcode == "NAVIGATE":
            lir_list.append(LIRNode("NAVIGATE", mir.operands))

        elif mir.opcode == "BUILD_DICT":
            lir_list.append(LIRNode("BUILD_DICT", [mir.operands[0]]))

        elif mir.opcode == "OP_ASYNC_CALL":
            lir_list.append(LIRNode("OP_ASYNC_CALL", [mir.operands[0], mir.operands[1]]))

        elif mir.opcode == "SET_BINDING":
            lir_list.append(LIRNode("SET_BINDING", [mir.operands[0]]))

        elif mir.opcode == "DECLARE_VALIDATION":
            lir_list.append(LIRNode("DECLARE_VALIDATION", [mir.operands[0]]))

        elif mir.opcode == "SET_ANIMATION":
            lir_list.append(LIRNode("SET_ANIMATION", [mir.operands[0]]))

        elif mir.opcode == "DECLARE_LIFECYCLE":
            body_lir = []
            for sub_mir in mir.operands[1]:
                self._mir_to_lir(sub_mir, body_lir)
            lir_list.append(LIRNode("DECLARE_LIFECYCLE", [mir.operands[0], body_lir]))
