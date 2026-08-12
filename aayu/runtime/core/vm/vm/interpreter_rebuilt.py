import time
from aayu.runtime.vm.instructions import Opcode
from aayu.runtime.vm.exceptions import KernelError
from aayu.runtime.vm.result import ResultStatus

class Interpreter:
    """Core bytecode dispatch loop."""
    def __init__(self, vm):
        self.vm = vm
        
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
                    raise KernelError("Division by zero")
                self.vm.value_stack.push(a / b)
                
            elif opcode == Opcode.STORE_STATE:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                name = self.vm.constant_pool[idx]
                val = self.vm.value_stack.pop()
                self.vm.state[name] = val
                
            elif opcode == Opcode.LOAD_STATE:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                name = self.vm.constant_pool[idx]
                val = self.vm.state.get(name, None)
                self.vm.value_stack.push(val)
                
            elif opcode == Opcode.BUILD_WIDGET:
                widget_type = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                props = self.vm.value_stack.pop()
                if widget_type == 0:
                    print(props)
                
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
                        if "authToken" in scope.variables:
                            token = scope.variables["authToken"]
                            break
                
                if not token:
                    raise KernelError("Unauthorized: Missing auth token", self.vm.registers.ip)
                    
                from aayu.runtime.stdlib.modules.auth_lib import verify_jwt
                payload = verify_jwt(token)
                if not payload:
                    raise KernelError("Unauthorized: Invalid or expired auth token", self.vm.registers.ip)
                    
                # Inject req_user into the local scope so the action can use it
                if self.vm.state_scopes:
                    self.vm.state_scopes[-1]["req_user"] = payload
                else:
                    self.vm.state["req_user"] = payload
                else:
                
            elif opcode == Opcode.RETURN_VALUE:
                self.vm.registers.ip += 3
                if self.vm.call_stack.depth() > 0:
                    ret_ip, is_comp = self.vm.call_stack.pop()
                    if is_comp:
                        self.vm.state_scopes.pop()
                    self.vm.registers.ip = ret_ip
                else:
                    return False
            elif opcode == Opcode.DECLARE_THEME:
                self.vm.registers.ip += 3
                props = self.vm.value_stack.pop()
                name = self.vm.value_stack.pop()
                from aayu.runtime.ui.theme import ThemeManager
                ThemeManager.instance().register_theme(name, props)
    
            elif opcode == Opcode.SET_THEME:
                self.vm.registers.ip += 3
                name = self.vm.value_stack.pop()
                from aayu.runtime.ui.theme import ThemeManager
                ThemeManager.instance().set_theme(name)
                
                try:
                    from aayu.runtime.renderers.web_renderer import WebRenderer
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
                    
            else:
                raise KernelError(f"Unknown opcode: 0x{opcode:02X} at IP: {self.vm.registers.ip}")
                
            return True

            elif opcode == Opcode.SETUP_EXCEPT:
                offset = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                if not hasattr(self.vm, 'block_stack'):
                    from aayu.runtime.vm.stack import Stack
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
                    raise KernelError(f"Unhandled AAYU Exception: {exc}")
                    
            elif opcode == Opcode.RETHROW:
                self.vm.registers.ip += 1
                exc = self.vm.value_stack.pop()
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
                    raise KernelError(f"Unhandled AAYU Exception: {exc}")

            elif opcode == Opcode.DISPATCH:
                # Kernel/Plugin invocation
                self.vm.registers.ip += 3
                try:
                    # Mock Kernel call
                    result = self.vm.kernel_dispatch()
                    if result.status == ResultStatus.ERROR:
                        raise KernelError(result.error_message)
                except KernelError as e:
                    # Exception Recovery gracefully catches it
                    print(f"Kernel caught exception: {e}")
                    # Push error to stack and continue instead of crashing
                    self.vm.value_stack.push(None)
                    
            else:
                self.vm.registers.ip += 3
                
        self.vm.profiler.end_time = time.time()
        
    def _run_assertions(self):
        assert self.vm.value_stack.depth() >= 0, "ASSERT Stack Underflow"
        assert self.vm.registers.ip >= 0, "ASSERT Instruction Pointer"
