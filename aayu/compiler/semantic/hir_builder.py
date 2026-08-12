from aayu.compiler.ast.nodes import (
    ProgramNode, StateDeclarationNode, LiteralNode,
    AssignmentNode, WidgetNode, ImportNode,
    ActionDeclarationNode, ActionCallNode, IdentifierNode,
    AppDeclarationNode, RunNode, IfNode, WhileNode, ForNode, BinaryOpNode,
    ModelDeclNode, RouteNode, ReturnNode, ThemeNode, UseThemeNode, NavigateNode,
    PropDeclarationNode, DictionaryNode, AwaitNode, BindNode, ValidateNode,
    AnimateNode, LifecycleNode, ArrayNode, SubscriptNode,
    TryNode, ThrowNode, RethrowNode
)
from aayu.compiler.semantic.symbols import SymbolTable, Symbol
from aayu.compiler.semantic.errors import SemanticError
from aayu.compiler.semantic.nodes import (
    SemanticProgramNode, SemanticStateDeclNode, SemanticLiteralNode,
    SemanticAssignmentNode, SemanticWidgetNode, SemanticImportNode,
    SemanticActionDeclNode, SemanticActionCallNode, SemanticIdentifierNode,
    SemanticIfNode, SemanticWhileNode, SemanticForNode, SemanticBinaryOpNode,
    SemanticModelFieldNode, SemanticRouteNode, SemanticMethodNode, SemanticReturnNode,
    SemanticThemeNode, SemanticUseThemeNode, SemanticNavigateNode, SemanticPropDeclNode,
    SemanticDictionaryNode, SemanticAwaitNode, SemanticBindNode, SemanticValidateNode,
    SemanticValidateFieldNode, SemanticValidationRuleNode, SemanticAnimateNode, SemanticLifecycleNode,
    SemanticArrayNode, SemanticSubscriptNode, SemanticModelDeclNode, SemanticModelAttributeNode,
    SemanticTryNode, SemanticThrowNode, SemanticRethrowNode
)

class HIRBuilder:
    def __init__(self, visiting_modules=None, asset_registry=None):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.visiting_modules = visiting_modules or set()
        self.asset_registry = asset_registry or {}

    def _analyze_if(self, node: IfNode):
        condition = self._analyze_node(node.condition)
        
        then_branch = []
        for stmt in node.then_branch:
            res = self._analyze_node(stmt)
            if res is not None: then_branch.append(res)
            
        else_branch = None
        if node.else_branch is not None:
            else_branch = []
            for stmt in node.else_branch:
                res = self._analyze_node(stmt)
                if res is not None: else_branch.append(res)
                
        return SemanticIfNode(line=node.line, column=node.column, scope=self.current_scope, condition=condition, then_branch=then_branch, else_branch=else_branch)

    def _analyze_while(self, node: WhileNode):
        condition = self._analyze_node(node.condition)
        
        # New scope for loop
        prev_scope = self.current_scope
        loop_scope = SymbolTable(parent=prev_scope)
        self.current_scope = loop_scope
        
        body = []
        for stmt in node.body:
            res = self._analyze_node(stmt)
            if res is not None: body.append(res)
            
        self.current_scope = prev_scope
        return SemanticWhileNode(line=node.line, column=node.column, scope=loop_scope, condition=condition, body=body)

    def _analyze_for(self, node: ForNode):
        iterable = self._analyze_node(node.iterable)
        
        # New scope for loop
        prev_scope = self.current_scope
        loop_scope = SymbolTable(parent=prev_scope)
        self.current_scope = loop_scope
        
        # Define iterator
        sym = Symbol(node.iterator, "local")
        self.current_scope.define(sym)
        if hasattr(node, 'index_name') and node.index_name:
            idx_sym = Symbol(node.index_name, "local")
            self.current_scope.define(idx_sym)
        
        body = []
        for stmt in node.body:
            res = self._analyze_node(stmt)
            if res is not None: body.append(res)
            
        self.current_scope = prev_scope
        
        index_name = getattr(node, 'index_name', None)
        return SemanticForNode(line=node.line, column=node.column, scope=loop_scope, iterator=node.iterator, iterable=iterable, body=body, index_name=index_name)

    def _analyze_binary_op(self, node: BinaryOpNode):
        left = self._analyze_node(node.left)
        right = self._analyze_node(node.right)
        return SemanticBinaryOpNode(line=node.line, column=node.column, scope=self.current_scope, left=left, op=node.operator, right=right)

    def build(self, ast: ProgramNode) -> SemanticProgramNode:
        statements = []
        for stmt in ast.statements:
            result = self._analyze_node(stmt)
            if result is not None:
                statements.append(result)
            
        return SemanticProgramNode(
            line=ast.line,
            column=ast.column,
            scope=self.global_scope,
            statements=statements
        )


    def _analyze_node(self, node):
        if isinstance(node, StateDeclarationNode):
            return self._analyze_state_decl(node)
        elif isinstance(node, AssignmentNode):
            return self._analyze_assignment(node)
        elif isinstance(node, LiteralNode):
            return self._analyze_literal(node)
        elif isinstance(node, WidgetNode):
            return self._analyze_widget(node)
        elif isinstance(node, ImportNode):
            return self._analyze_import(node)
        elif isinstance(node, ActionDeclarationNode):
            return self._analyze_action_decl(node)
        elif isinstance(node, ActionCallNode):
            return self._analyze_action_call(node)
        elif isinstance(node, ArrayNode):
            return self._analyze_array(node)
        elif isinstance(node, DictionaryNode):
            pairs = {}
            for k, v in node.pairs.items():
                pairs[k] = self._analyze_node(v)
            return SemanticDictionaryNode(line=node.line, column=node.column, scope=self.current_scope, pairs=pairs)
        elif isinstance(node, SubscriptNode):
            return self._analyze_subscript(node)
        elif isinstance(node, IdentifierNode):
            return self._analyze_identifier(node)
        elif isinstance(node, IfNode):
            return self._analyze_if(node)
        elif isinstance(node, WhileNode):
            return self._analyze_while(node)
        elif isinstance(node, ForNode):
            return self._analyze_for(node)
        elif isinstance(node, BinaryOpNode):
            return self._analyze_binary_op(node)
        elif isinstance(node, ReturnNode):
            return self._analyze_return(node)
        elif isinstance(node, AwaitNode):
            return SemanticAwaitNode(
                line=node.line, column=node.column,
                expression=self._analyze_node(node.expression),
                scope=self.current_scope
            )
        elif isinstance(node, TryNode):
            return self._analyze_try(node)
        elif isinstance(node, ThrowNode):
            return self._analyze_throw(node)
        elif isinstance(node, RethrowNode):
            return self._analyze_rethrow(node)
        elif isinstance(node, ModelDeclNode):
            return self._analyze_model(node)
        elif isinstance(node, RouteNode):
            return self._analyze_route(node)
        elif isinstance(node, AppDeclarationNode):
            # App declaration is metadata — pass through as-is
            return None
        elif isinstance(node, RunNode):
            # Run is a control marker — skip in semantic analysis
            return None
        elif isinstance(node, ThemeNode):
            return SemanticThemeNode(line=node.line, column=node.column, scope=self.current_scope, name=node.name, properties=node.properties)
        elif isinstance(node, UseThemeNode):
            return SemanticUseThemeNode(line=node.line, column=node.column, scope=self.current_scope, name=node.name)
        elif isinstance(node, NavigateNode):
            kwargs = {}
            for k, v in node.kwargs.items():
                kwargs[k] = self._analyze_node(v)
            return SemanticNavigateNode(line=node.line, column=node.column, scope=self.current_scope, target=node.target, kwargs=kwargs)
        elif isinstance(node, PropDeclarationNode):
            sym = Symbol(node.name, "prop")
            self.current_scope.define(sym)
            return SemanticPropDeclNode(line=node.line, column=node.column, scope=self.current_scope, name=node.name)
        elif isinstance(node, BindNode):
            return SemanticBindNode(line=node.line, column=node.column, scope=self.current_scope, target=node.target)
        elif isinstance(node, ValidateNode):
            semantic_fields = []
            for field in node.fields:
                semantic_rules = []
                for rule in field.rules:
                    s_args = [self._analyze_node(a) for a in rule.args]
                    semantic_rules.append(SemanticValidationRuleNode(rule=rule.rule, args=s_args))
                semantic_fields.append(SemanticValidateFieldNode(field_name=field.field_name, rules=semantic_rules))
            return SemanticValidateNode(line=node.line, column=node.column, scope=self.current_scope, fields=semantic_fields)
        elif isinstance(node, AnimateNode):
            props = {}
            for k, v in node.properties.items():
                props[k] = self._analyze_node(v)
            return SemanticAnimateNode(line=node.line, column=node.column, scope=self.current_scope, properties=props)
        elif isinstance(node, LifecycleNode):
            body = []
            for stmt in node.body:
                res = self._analyze_node(stmt)
                if res is not None: body.append(res)
            return SemanticLifecycleNode(line=node.line, column=node.column, scope=self.current_scope, hook=node.hook, body=body)
        else:
            raise SemanticError(f"Unknown node type: {type(node).__name__}", getattr(node, 'line', 0), getattr(node, 'column', 0))

    def _analyze_action_decl(self, node: ActionDeclarationNode):
        statements = []
        for stmt in node.statements:
            statements.append(self._analyze_node(stmt))
            
        from aayu.compiler.semantic.nodes import SemanticDecoratorNode
        sem_decorators = []
        for d in getattr(node, "decorators", []):
            sem_decorators.append(SemanticDecoratorNode(name=d.name, args=d.args))
            
        return SemanticActionDeclNode(
            line=node.line, column=node.column, scope=self.current_scope,
            name=node.name, statements=statements, args=[a.name for a in node.args],
            decorators=sem_decorators
        )

    def _analyze_action_call(self, node: ActionCallNode):
        args = []
        for a in node.args:
            args.append(self._analyze_node(a))
        if node.name and node.name[0].isupper():
            from aayu.compiler.semantic.nodes import SemanticWidgetNode
            # It's a widget like Text(val) or Button("Click")
            props = {}
            if args:
                props["value"] = args[0]
            # Since action call doesn't have keyword args in AST yet, we assume value is first arg
            return SemanticWidgetNode(
                line=node.line, column=node.column, scope=self.current_scope,
                widget_type=node.name, props=props, children=[]
            )
            
        return SemanticActionCallNode(
            line=node.line, column=node.column, scope=self.current_scope,
            name=node.name, args=args
        )

    def _analyze_dictionary(self, node: DictionaryNode):
        pairs = {}
        for key, value_node in node.pairs.items():
            pairs[key] = self._analyze_node(value_node)
        return SemanticDictionaryNode(
            line=node.line, column=node.column, scope=self.current_scope,
            pairs=pairs
        )

    def _analyze_subscript(self, node: SubscriptNode):
        target = self._analyze_node(node.target)
        index = self._analyze_node(node.index)
        return SemanticSubscriptNode(
            line=node.line, column=node.column, scope=self.current_scope,
            target=target, index=index
        )

    def _analyze_identifier(self, node: IdentifierNode):
        if node.name.startswith("Theme."):
            css_var = f"var(--{node.name.split('.')[1]})"
            return SemanticLiteralNode(
                line=node.line, column=node.column, scope=self.current_scope,
                value=css_var, type_name="String"
            )
        return SemanticIdentifierNode(
            line=node.line, column=node.column, scope=self.current_scope,
            name=node.name
        )

    def _analyze_state_decl(self, node: StateDeclarationNode):
        if self.current_scope.resolve(node.name) is not None:
            raise SemanticError(f"Duplicate declaration of '{node.name}'", node.line, node.column)
            
        sym = Symbol(node.name, "state")
        self.current_scope.define(sym)
        
        val_node = self._analyze_node(node.value)
        return SemanticStateDeclNode(
            line=node.line,
            column=node.column,
            scope=self.current_scope,
            name=node.name,
            value=val_node
        )

    def _analyze_assignment(self, node: AssignmentNode):
        if self.current_scope.resolve(node.target) is None:
            sym = Symbol(node.target, "local")
            self.current_scope.define(sym)
            
        val_node = self._analyze_node(node.value)
        return SemanticAssignmentNode(
            line=node.line,
            column=node.column,
            scope=self.current_scope,
            target=node.target,
            value=val_node
        )

    def _analyze_literal(self, node: LiteralNode):
        if isinstance(node.value, list):
            resolved = []
            for item in node.value:
                res = self._analyze_node(item)
                # For literal arrays, we actually want raw python values if possible?
                # Actually, wait. AAYU's ConstantPool expects raw values. Let's extract values if they are literals!
                # If they are NOT literals, this is an expression list (e.g. [1, a, 2+3]), which needs a BUILD_LIST opcode!
                # But for now, since we only need simple arrays, let's just make it a list of SemanticNodes or raw values?
                if isinstance(item, LiteralNode):
                    resolved.append(item.value)
                else:
                    # Let's just append the raw node value string for now if it's complex
                    resolved.append(str(item))
            t_name = "list"
            val = resolved
        else:
            t_name = "number" if str(node.value).isdigit() else "string"
            val = node.value
            if isinstance(val, str) and val in self.asset_registry:
                val = self.asset_registry[val]
            
        return SemanticLiteralNode(
            line=node.line,
            column=node.column,
            scope=self.current_scope,
            value=val,
            type_name=t_name
        )

    def _analyze_widget(self, node: WidgetNode):
        from aayu.compiler.semantic.nodes import SemanticWidgetNode
        from aayu.compiler.ast.nodes import IdentifierNode
        # We can validate widget types here
        children = []
        new_props = {}
        for c in node.children:
            analyzed_c = self._analyze_node(c)
            # If it's a property node (lowercase/camelCase widget type that isn't a known structural block)
            if isinstance(analyzed_c, SemanticWidgetNode) and (analyzed_c.widget_type[0].islower() if analyzed_c.widget_type else False) and analyzed_c.widget_type not in ["center", "expanded", "padding"]:
                prop_val = analyzed_c.props.get("value_node", analyzed_c.props.get("text", None))
                from aayu.compiler.semantic.nodes import SemanticActionCallNode, SemanticClosureNode
                
                if isinstance(prop_val, SemanticActionCallNode):
                    prop_val = SemanticClosureNode(line=prop_val.line, column=prop_val.column, scope=self.current_scope, action_name=prop_val.name, args=prop_val.args)
                elif not prop_val and analyzed_c.children:
                    child = analyzed_c.children[0]
                    if isinstance(child, SemanticActionCallNode):
                        prop_val = SemanticClosureNode(line=child.line, column=child.column, scope=self.current_scope, action_name=child.name, args=child.args)
                    else:
                        prop_val = child
                
                if prop_val is not None:
                    # If it's an IdentifierNode, we keep it as an IdentifierNode for the VM/IRPipeline to handle
                    new_props[analyzed_c.widget_type] = prop_val.name if hasattr(prop_val, "name") else prop_val
                else:
                    new_props[analyzed_c.widget_type] = True # boolean flag property without value
            else:
                children.append(analyzed_c)

        responsive = {}
        for k, v in node.props.items():
            if k.endswith("_mobile"):
                base = k[:-7]
                if base not in responsive: responsive[base] = {}
                responsive[base]["mobile"] = v
            elif k.endswith("_tablet"):
                base = k[:-7]
                if base not in responsive: responsive[base] = {}
                responsive[base]["tablet"] = v
            elif k.endswith("_desktop"):
                base = k[:-8]
                if base not in responsive: responsive[base] = {}
                responsive[base]["desktop"] = v
            else:
                if hasattr(v, "line"):
                    analyzed_v = self._analyze_node(v)
                    from aayu.compiler.semantic.nodes import SemanticActionCallNode, SemanticClosureNode
                    if k.startswith("on") and isinstance(analyzed_v, SemanticActionCallNode):
                        analyzed_v = SemanticClosureNode(line=v.line, column=v.column, scope=self.current_scope, action_name=analyzed_v.name, args=analyzed_v.args)
                    new_props[k] = analyzed_v
                else:
                    new_props[k] = v
        if responsive:
            new_props["__responsive__"] = responsive
            
        return SemanticWidgetNode(
            line=node.line,
            column=node.column,
            scope=self.current_scope,
            widget_type=node.widget_type,
            props=new_props,
            children=children
        )

    def _analyze_import(self, node: ImportNode):
        from aayu.compiler.errors import CompilerError
        if node.module in self.visiting_modules:
            raise CompilerError(f"Import cycle detected: '{node.module}'", node.line, getattr(node, 'column', 0))
            
        self.visiting_modules.add(node.module)
        # In a real compiler, we would load and parse the module here, and run SemanticAnalyzer recursively
        # For now, we just track the cycle.
        return SemanticImportNode(
            line=node.line,
            column=getattr(node, 'column', 0),
            scope=self.current_scope,
            module=node.module
        )

    def _analyze_model(self, node: ModelDeclNode):
        semantic_fields = []
        for field in node.fields:
            if field.field_type not in ["String", "Int", "Boolean", "Float", "List", "Dict"]:
                # Could register custom models here or ensure it's a known model for relations
                pass
            
            semantic_attrs = []
            for attr in field.attributes:
                semantic_attrs.append(SemanticModelAttributeNode(name=attr.name, args=attr.args))
                
            semantic_fields.append(SemanticModelFieldNode(
                name=field.name, 
                field_type=field.field_type,
                attributes=semantic_attrs
            ))
            
        sym = Symbol(node.name, "model")
        self.current_scope.define(sym)
        
        return SemanticModelDeclNode(
            line=node.line, column=node.column, scope=self.current_scope,
            name=node.name,
            fields=semantic_fields,
            decorators=node.decorators
        )

    def _analyze_route(self, node: RouteNode):
        methods = []
        for method in node.methods:
            # New scope for route method body
            prev_scope = self.current_scope
            method_scope = SymbolTable(parent=prev_scope)
            self.current_scope = method_scope
            
            body = []
            for stmt in method.body:
                res = self._analyze_node(stmt)
                if res is not None: body.append(res)
                
            self.current_scope = prev_scope
            
            methods.append(SemanticMethodNode(
                line=method.line, column=method.column, scope=method_scope,
                method=method.method, body=body
            ))
            
        return SemanticRouteNode(
            line=node.line, column=node.column, scope=self.current_scope,
            path=node.path, methods=methods
        )

    def _analyze_return(self, node: ReturnNode):
        val = self._analyze_node(node.value)
        return SemanticReturnNode(
            line=node.line, column=node.column, scope=self.current_scope,
            value=val
        )

    def _analyze_array(self, node):
        from aayu.compiler.semantic.nodes import SemanticArrayNode
        elements = [self._analyze_node(el) for el in node.elements]
        return SemanticArrayNode(line=node.line, column=node.column, scope=self.current_scope, elements=elements)

    def _analyze_try(self, node: TryNode):
        try_block = [self._analyze_node(stmt) for stmt in node.try_block]
        
        catch_block = []
        if node.catch_block:
            prev_scope = self.current_scope
            self.current_scope = SymbolTable(parent=self.current_scope)
            if node.catch_var:
                self.current_scope.define(Symbol(node.catch_var, "Any"))
            catch_block = [self._analyze_node(stmt) for stmt in node.catch_block]
            self.current_scope = prev_scope
            
        finally_block = []
        if node.finally_block:
            finally_block = [self._analyze_node(stmt) for stmt in node.finally_block]
            
        from aayu.compiler.semantic.nodes import SemanticTryNode
        return SemanticTryNode(
            line=node.line, column=node.column, scope=self.current_scope,
            try_block=try_block, catch_var=node.catch_var,
            catch_block=catch_block, finally_block=finally_block
        )

    def _analyze_throw(self, node: ThrowNode):
        value = self._analyze_node(node.value)
        from aayu.compiler.semantic.nodes import SemanticThrowNode
        return SemanticThrowNode(line=node.line, column=node.column, scope=self.current_scope, value=value)

    def _analyze_rethrow(self, node: RethrowNode):
        from aayu.compiler.semantic.nodes import SemanticRethrowNode
        return SemanticRethrowNode(line=node.line, column=node.column, scope=self.current_scope)
