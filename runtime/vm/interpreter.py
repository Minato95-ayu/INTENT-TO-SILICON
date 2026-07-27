import time
from runtime.vm.instructions import Opcode
from runtime.vm.exceptions import KernelError
from runtime.vm.exceptions import KernelError
from runtime.vm.result import ResultStatus
from runtime.renderers.web_renderer import RenderNode

class Interpreter:
    """Core bytecode dispatch loop."""
    def __init__(self, vm):
        self.vm = vm
        self.node_stack = []
        from runtime.ui.render_tree import RenderTree
        self.render_tree = RenderTree()
        
    def build_stacktrace(self):
        trace = []
        for ip, is_comp in reversed(self.vm.call_stack.stack):
            trace.append({
                "action": "component" if is_comp else "function",
                "ip": ip,
                "line": -1
            })
        return trace
        
    def _throw_exception(self, exc):
        from runtime.vm.exceptions import AayuException, InternalException
        if not isinstance(exc, AayuException):
            exc = InternalException(str(exc))
            
        exc.stacktrace = self.build_stacktrace()
        handled = False
        
        if hasattr(self.vm, 'block_stack'):
            while self.vm.block_stack.depth() > 0:
                block = self.vm.block_stack.pop()
                if block["type"] == "TRY":
                    while self.vm.value_stack.depth() > block["stack_depth"]:
                        self.vm.value_stack.pop()
                    self.vm.value_stack.push(exc)
                    self.vm.registers.ip = block["handler_ip"]
                    handled = True
                    break
                    
        if not handled:
            mode = getattr(self.vm.config, 'mode', 'SERVER')
            if mode == 'CLI':
                print(f"[AAYU PANIC] {exc.exc_type}: {exc.message}")
                import sys; sys.exit(1)
            else:
                raise exc
        
    def run(self):
        self.vm.profiler.start_time = time.time()
        
        while True:
            # Infinite loop timeout check (dev mode)
            if self.vm.config.timeout_ms > 0:
                elapsed = (time.time() - self.vm.profiler.start_time) * 1000
                if elapsed > self.vm.config.timeout_ms:
                    print(f"Warning: Loop running for {self.vm.config.timeout_ms}ms. Terminating.")
                    break
                    
            if self.vm.config.debug_mode and self.vm.config.enable_assertions:
                self._run_assertions()
                
            self.vm.debugger.check_breakpoint()
            
            opcode = self.vm.decoder.fetch8(self.vm.registers.ip)
            print(f"[VM TRACE] IP={self.vm.registers.ip} Opcode={opcode:02X} depth={self.vm.call_stack.depth()}")
            
            # Profiler tick
            self.vm.profiler.tick(len(self.vm.heap.allocator.pool.pool) * 64)
            
            if opcode == Opcode.HALT:
                break
                
            elif opcode == Opcode.PUSH_CONST:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                val = self.vm.constant_pool[idx]
                self.vm.value_stack.push(val)
                
            elif opcode == Opcode.POP:
                self.vm.registers.ip += 3
                self.vm.value_stack.pop()
                
            elif opcode == Opcode.ADD:
                self.vm.registers.ip += 3
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                if isinstance(a, str) or isinstance(b, str):
                    self.vm.value_stack.push(str(a) + str(b))
                else:
                    self.vm.value_stack.push(a + b)
                
            elif opcode == Opcode.SUB:
                self.vm.registers.ip += 3
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a - b)
                
            elif opcode == Opcode.MUL:
                self.vm.registers.ip += 3
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a * b)
                
            elif opcode == Opcode.DIV:
                self.vm.registers.ip += 3
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                if b == 0:
                    from runtime.vm.exceptions import RuntimeException
                    self._throw_exception(RuntimeException("Division by zero", code="AYU-1001"))
                    continue
                self.vm.value_stack.push(a / b)
                
            elif opcode == Opcode.CMP_EQ:
                self.vm.registers.ip += 3
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                print(f"[VM DEBUG] CMP_EQ: {repr(a)} == {repr(b)}")
                self.vm.value_stack.push(a == b)
                
            elif opcode == Opcode.CMP_NEQ:
                self.vm.registers.ip += 3
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a != b)
                
            elif opcode == Opcode.CMP_LT:
                self.vm.registers.ip += 3
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a < b)
                
            elif opcode == Opcode.CMP_GT:
                self.vm.registers.ip += 3
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a > b)
                
            elif opcode == Opcode.CMP_LTE:
                self.vm.registers.ip += 3
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a <= b)
                
            elif opcode == Opcode.CMP_GTE:
                self.vm.registers.ip += 3
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a >= b)
                
            elif opcode == Opcode.STORE_STATE:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                name = self.vm.constant_pool[idx]
                val = self.vm.value_stack.pop()
                self.vm.update_state(name, val)
                
            elif opcode == Opcode.LOAD_STATE:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                name = self.vm.constant_pool[idx]
                val = None
                for scope in reversed(self.vm.state_scopes):
                    if name in scope:
                        val = scope[name]
                        break
                self.vm.value_stack.push(val)
                
            elif opcode == Opcode.INIT_STATE:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                name = self.vm.constant_pool[idx]
                val = self.vm.value_stack.pop()
                found = False
                for scope in reversed(self.vm.state_scopes):
                    if name in scope:
                        found = True
                        break
                if not found:
                    self.vm.state[name] = val
                
            elif opcode == Opcode.CALL_COMPONENT:
                target = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.call_stack.push((self.vm.registers.ip + 3, True))
                props = self.vm.value_stack.pop()
                scope = {}
                if isinstance(props, dict):
                    for k, v in props.items():
                        scope[k] = v
                if hasattr(self.vm, 'state_scopes'):
                    self.vm.state_scopes.append(scope)
                self.vm.registers.ip = target

            elif opcode == Opcode.CALL:
                target = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.call_stack.push((self.vm.registers.ip + 3, False))
                self.vm.registers.ip = target

            elif opcode == Opcode.MARK_BLOCK_START:
                self.vm.registers.ip += 3
                self.node_stack.append("$BLOCK_START")

            elif opcode == Opcode.CREATE_CLOSURE:
                num_args = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                action_name = self.vm.value_stack.pop()
                args = []
                for _ in range(num_args):
                    args.insert(0, self.vm.value_stack.pop())
                closure = {"name": action_name, "args": args}
                self.vm.value_stack.push(closure)

            elif opcode == Opcode.BUILD_WIDGET:
                widget_type = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                props = self.vm.value_stack.pop()
                
                # Resolve $STACK markers in props
                if isinstance(props, dict):
                    stack_keys = [k for k, v in props.items() if v == "$STACK"]
                    if stack_keys:
                        props = props.copy()  # Shallow copy is sufficient since $STACK markers are only at top-level
                        for key in reversed(stack_keys):
                            props[key] = self.vm.value_stack.pop()
                
                from compiler.bytecode.encoder import WIDGET_TYPES
                widget_name = next((k for k, v in WIDGET_TYPES.items() if v == widget_type), "UNKNOWN")
                
                is_block = widget_name.lower() in [
                    "container", "row", "column", "card", "stack", "center",
                    "expanded", "padding", "scrollview", "grid",
                    "appbar", "navigationbar", "list", "form", "dialog",
                    "drawer", "snackbar", "tabbar", "scaffold", "page", "component"
                ]
                
                children = []
                if is_block:
                    while self.node_stack and self.node_stack[-1] != "$BLOCK_START":
                        children.insert(0, self.node_stack.pop())
                    if self.node_stack and self.node_stack[-1] == "$BLOCK_START":
                        self.node_stack.pop()
                        
                node = RenderNode(widget_name, props=props)
                node.children = children
                if widget_name == "PAGE":
                    self.render_tree.root = node
                else:
                    self.node_stack.append(node)
                
            elif opcode == Opcode.PRINT:
                self.vm.registers.ip += 3
                val = self.vm.value_stack.pop()
                print(val)
                
            elif opcode == Opcode.JMP_IF_FALSE:
                target = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                cond = self.vm.value_stack.pop()
                if not cond:
                    self.vm.registers.ip = target
                else:
                    self.vm.registers.ip += 3
                    
            elif opcode == Opcode.JMP:
                target = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip = target
                

            elif opcode == Opcode.CREATE_MODEL:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                model_name = self.vm.value_stack.pop()
                fields = self.vm.constant_pool[idx]
                self.vm.database.create_model(model_name, fields)
                
            elif opcode == Opcode.REGISTER_ROUTE:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                path = self.vm.value_stack.pop()
                methods_meta = self.vm.constant_pool[idx]
                self.vm.api_router.register_route(path, methods_meta)
                self.vm.api_router.start()
                
            elif opcode == Opcode.CHECK_AUTH:
                self.vm.registers.ip += 3
                # Check for authToken in the current state scope
                token = None
                if self.vm.state_scopes:
                    # We search from top to bottom
                    for scope in reversed(self.vm.state_scopes):
                        if "authToken" in scope:
                            token = scope["authToken"]
                            break
                
                if not token:
                    token = self.vm.state.get("authToken")
                
                if not token:
                    from runtime.vm.exceptions import AuthenticationException
                    self._throw_exception(AuthenticationException("Missing auth token", code="AYU-2001"))
                    continue
                    
                from runtime.stdlib.modules.auth_lib import verify_jwt
                payload = verify_jwt(token)
                if not payload:
                    from runtime.vm.exceptions import AuthenticationException
                    self._throw_exception(AuthenticationException("Invalid or expired auth token", code="AYU-2001"))
                    continue
                    
                # Inject req_user into the local scope so the action can use it
                if self.vm.state_scopes:
                    self.vm.state_scopes[-1]["req_user"] = payload
                else:
                    self.vm.state["req_user"] = payload
            elif opcode == Opcode.RETURN_VALUE or opcode == Opcode.RET:
                if opcode == Opcode.RETURN_VALUE:
                    self.vm.registers.ip += 3
                if self.vm.call_stack.depth() > 0:
                    ret_ip, is_comp = self.vm.call_stack.pop()
                    if is_comp:
                        if hasattr(self.vm, 'state_scopes') and self.vm.state_scopes:
                            self.vm.state_scopes.pop()
                        if self.node_stack:
                            self.node_stack.pop()
                    self.vm.registers.ip = ret_ip
                else:
                    return False
            elif opcode == Opcode.DECLARE_THEME:
                self.vm.registers.ip += 3
                props = self.vm.value_stack.pop()
                name = self.vm.value_stack.pop()
                from runtime.ui.theme import ThemeManager
                ThemeManager.instance().register_theme(name, props)
    
            elif opcode == Opcode.SET_THEME:
                self.vm.registers.ip += 3
                name = self.vm.value_stack.pop()
                from runtime.ui.theme import ThemeManager
                ThemeManager.instance().set_theme(name)
                
                try:
                    from runtime.renderers.web_renderer import WebRenderer
                    if getattr(WebRenderer, '_instance', None) is not None:
                        WebRenderer.instance().broadcast_theme_update(name)
                except ImportError:
                    pass
    
            elif opcode == Opcode.NAVIGATE:
                num_args = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                
                keys = self.vm.value_stack.pop()
                target = self.vm.value_stack.pop()
                
                params = {}
                if keys:
                    for key in reversed(keys):
                        params[key] = self.vm.value_stack.pop()
                        
                self.vm.router.navigate(target, params)
                
            elif opcode == Opcode.BUILD_DICT:
                self.vm.registers.ip += 3
                keys = self.vm.value_stack.pop()
                d = {}
                print(f"[DEBUG BUILD_DICT] keys: {keys}, stack depth: {self.vm.value_stack.depth()}")
                for key in reversed(keys):
                    try:
                        d[key] = self.vm.value_stack.pop()
                    except Exception as e:
                        print(f"[DEBUG BUILD_DICT ERROR] Failed popping for key: {key}. Current stack: {self.vm.value_stack.stack}")
                        raise e
                self.vm.value_stack.push(d)
                
            elif opcode == Opcode.OP_ASYNC_CALL:
                # Opcode.OP_ASYNC_CALL num_args
                # Stack top has: argN, argN-1, ... arg1, name_idx
                num_args = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                
                func_name = self.vm.value_stack.pop()
                args = []
                for _ in range(num_args):
                    args.insert(0, self.vm.value_stack.pop())
                
                stdlib = self.vm.stdlib
                
                # Find function in registry
                if func_name in stdlib.registry.functions:
                    func = stdlib.registry.functions[func_name]
                    result = func(args, self.vm)
                    self.vm.value_stack.push(result)
                elif isinstance(func_name, str) and "." in func_name:
                    parts = func_name.split(".")
                    target_name = parts[0]
                    method_name = parts[1]
                    target = None
                    for scope in reversed(self.vm.state_scopes):
                        if target_name in scope:
                            target = scope[target_name]
                            break
                    if target is not None:
                        dispatch_name = f"__method_{method_name}"
                        args.insert(0, target)
                        if dispatch_name in stdlib.registry.functions:
                            func = stdlib.registry.functions[dispatch_name]
                            result = func(args, self.vm)
                            self.vm.value_stack.push(result)
                        else:
                            print(f"[VM Warning] Unresolved native method call: {func_name}")
                            self.vm.value_stack.push(None)
                    else:
                        print(f"[VM Warning] Unresolved target for method call: {func_name}")
                        self.vm.value_stack.push(None)
                else:
                    print(f"[VM Warning] Unresolved native function call: {func_name}")
                    self.vm.value_stack.push(None)
                
            elif opcode == Opcode.SET_BINDING:
                self.vm.registers.ip += 3
                target = self.vm.value_stack.pop()
                self.node_stack.append(RenderNode("BINDING", props={"target": target}))
            elif opcode == Opcode.DECLARE_VALIDATION:
                self.vm.registers.ip += 3
                fields = self.vm.value_stack.pop()
                self.node_stack.append(RenderNode("VALIDATION", props={"fields": fields}))
                    
            elif opcode == Opcode.SET_ANIMATION:
                self.vm.registers.ip += 3
                keys = self.vm.value_stack.pop()
                anim_props = {}
                for key in reversed(keys):
                    anim_props[key] = self.vm.value_stack.pop()
                self.node_stack.append(RenderNode("ANIMATION", props={"props": anim_props}))
                    
            elif opcode == Opcode.DECLARE_LIFECYCLE:
                offset = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                hook = self.vm.value_stack.pop()
                if self.vm.state_scopes:
                    self.vm.state_scopes[-1][f"__lifecycle_{hook}__"] = offset
    
            elif opcode == Opcode.CREATE_ARRAY:
                count = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                elements = []
                for _ in range(count):
                    elements.insert(0, self.vm.value_stack.pop())
                self.vm.value_stack.push(elements)
                    
            elif opcode == Opcode.GET_LENGTH:
                self.vm.registers.ip += 3
                val = self.vm.value_stack.pop()
                if isinstance(val, (list, str, dict)):
                    self.vm.value_stack.push(len(val))
                else:
                    self.vm.value_stack.push(0)
                    
            elif opcode == Opcode.LOAD_SUBSCR:
                self.vm.registers.ip += 3
                index = self.vm.value_stack.pop()
                container = self.vm.value_stack.pop()
                try:
                    val = container[index]
                except (IndexError, KeyError, TypeError):
                    val = None
                self.vm.value_stack.push(val)
                
            elif opcode == Opcode.STORE_SUBSCR:
                self.vm.registers.ip += 3
                index = self.vm.value_stack.pop()
                container = self.vm.value_stack.pop()
                value = self.vm.value_stack.pop()
                try:
                    container[index] = value
                except (IndexError, KeyError, TypeError):
                    pass
                    
            elif opcode == Opcode.SETUP_EXCEPT:
                offset = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                if not hasattr(self.vm, 'block_stack'):
                    from runtime.vm.stack import Stack
                    self.vm.block_stack = Stack(max_depth=64)
                self.vm.block_stack.push({
                    "type": "TRY",
                    "handler_ip": offset,
                    "stack_depth": self.vm.value_stack.depth()
                })
                
            elif opcode == Opcode.POP_EXCEPT:
                self.vm.registers.ip += 1
                if hasattr(self.vm, 'block_stack') and self.vm.block_stack.depth() > 0:
                    block = self.vm.block_stack.pop()
                    if block["type"] != "TRY":
                        raise KernelError("POP_EXCEPT called but top block is not TRY")
                        
            elif opcode == Opcode.THROW:
                self.vm.registers.ip += 1
                exc = self.vm.value_stack.pop()
                self._throw_exception(exc)
                
            elif opcode == Opcode.RETHROW:
                self.vm.registers.ip += 1
                exc = self.vm.value_stack.pop()
                self._throw_exception(exc)
                
            elif opcode == Opcode.SETUP_FINALLY:
                offset = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                if not hasattr(self.vm, 'block_stack'):
                    from runtime.vm.stack import Stack
                    self.vm.block_stack = Stack(max_depth=64)
                self.vm.block_stack.push({
                    "type": "FINALLY",
                    "handler_ip": offset,
                    "stack_depth": self.vm.value_stack.depth()
                })
                
            elif opcode == Opcode.EXEC_FINALLY:
                self.vm.registers.ip += 1
                # Execute finally logic (handled by compiler mostly, this just pops the block)
                if hasattr(self.vm, 'block_stack') and self.vm.block_stack.depth() > 0:
                    block = self.vm.block_stack.pop()
                    if block["type"] != "FINALLY":
                        pass
                    
            else:
                raise KernelError(f"Unknown opcode: 0x{opcode:02X} at IP: {self.vm.registers.ip}")
                
        self.vm.profiler.end_time = time.time()
        
    def _run_assertions(self):
        assert self.vm.value_stack.depth() >= 0, "ASSERT Stack Underflow"
        assert self.vm.registers.ip >= 0, "ASSERT Instruction Pointer"
