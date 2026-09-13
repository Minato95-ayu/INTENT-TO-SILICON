import time
from runtime.vm.instructions import Opcode
from runtime.vm.exceptions import KernelError
from runtime.vm.exceptions import KernelError
from runtime.vm.result import ResultStatus
from runtime.renderers.web_renderer import RenderNode

class Interpreter:
    'Core bytecode dispatch loop.'

    def __init__(self, vm):
        self.vm = vm
        self.node_stack = []
        from runtime.ui.render_tree import RenderTree
        self.render_tree = RenderTree()
        self.dispatch_table = [None] * 256
        self.dispatch_table[Opcode.HALT] = self.op_HALT
        self.dispatch_table[Opcode.PUSH_CONST] = self.op_PUSH_CONST
        self.dispatch_table[Opcode.POP] = self.op_POP
        self.dispatch_table[Opcode.ADD] = self.op_ADD
        self.dispatch_table[Opcode.SUB] = self.op_SUB
        self.dispatch_table[Opcode.MUL] = self.op_MUL
        self.dispatch_table[Opcode.DIV] = self.op_DIV
        self.dispatch_table[Opcode.CMP_EQ] = self.op_CMP_EQ
        self.dispatch_table[Opcode.CMP_NEQ] = self.op_CMP_NEQ
        self.dispatch_table[Opcode.CMP_LT] = self.op_CMP_LT
        self.dispatch_table[Opcode.CMP_GT] = self.op_CMP_GT
        self.dispatch_table[Opcode.CMP_LTE] = self.op_CMP_LTE
        self.dispatch_table[Opcode.CMP_GTE] = self.op_CMP_GTE
        self.dispatch_table[Opcode.STORE_STATE] = self.op_STORE_STATE
        self.dispatch_table[Opcode.LOAD_STATE] = self.op_LOAD_STATE
        self.dispatch_table[Opcode.INIT_STATE] = self.op_INIT_STATE
        self.dispatch_table[Opcode.CALL_COMPONENT] = self.op_CALL_COMPONENT
        self.dispatch_table[Opcode.PREPARE_CALL] = self.op_PREPARE_CALL
        self.dispatch_table[Opcode.CALL] = self.op_CALL
        self.dispatch_table[Opcode.MARK_BLOCK_START] = self.op_MARK_BLOCK_START
        self.dispatch_table[Opcode.CREATE_CLOSURE] = self.op_CREATE_CLOSURE
        self.dispatch_table[Opcode.BUILD_WIDGET] = self.op_BUILD_WIDGET
        self.dispatch_table[Opcode.PRINT] = self.op_PRINT
        self.dispatch_table[Opcode.JMP_IF_FALSE] = self.op_JMP_IF_FALSE
        self.dispatch_table[Opcode.JMP] = self.op_JMP
        self.dispatch_table[Opcode.CREATE_MODEL] = self.op_CREATE_MODEL
        self.dispatch_table[Opcode.REGISTER_ROUTE] = self.op_REGISTER_ROUTE
        self.dispatch_table[Opcode.CHECK_AUTH] = self.op_CHECK_AUTH
        self.dispatch_table[Opcode.DB_INSERT] = self.op_DB_INSERT
        self.dispatch_table[Opcode.DB_FIND] = self.op_DB_FIND
        self.dispatch_table[Opcode.RESPOND] = self.op_RESPOND
        self.dispatch_table[Opcode.RETURN_VALUE] = self.op_RETURN_VALUE
        self.dispatch_table[Opcode.RET] = self.op_RET
        self.dispatch_table[Opcode.DECLARE_THEME] = self.op_DECLARE_THEME
        self.dispatch_table[Opcode.SET_THEME] = self.op_SET_THEME
        self.dispatch_table[Opcode.NAVIGATE] = self.op_NAVIGATE
        self.dispatch_table[Opcode.BUILD_DICT] = self.op_BUILD_DICT
        self.dispatch_table[Opcode.OP_ASYNC_CALL] = self.op_OP_ASYNC_CALL
        self.dispatch_table[Opcode.SET_BINDING] = self.op_SET_BINDING
        self.dispatch_table[Opcode.DECLARE_VALIDATION] = self.op_DECLARE_VALIDATION
        self.dispatch_table[Opcode.SET_ANIMATION] = self.op_SET_ANIMATION
        self.dispatch_table[Opcode.DECLARE_LIFECYCLE] = self.op_DECLARE_LIFECYCLE
        self.dispatch_table[Opcode.CREATE_ARRAY] = self.op_CREATE_ARRAY
        self.dispatch_table[Opcode.GET_LENGTH] = self.op_GET_LENGTH
        self.dispatch_table[Opcode.LOAD_SUBSCR] = self.op_LOAD_SUBSCR
        self.dispatch_table[Opcode.STORE_SUBSCR] = self.op_STORE_SUBSCR
        self.dispatch_table[Opcode.SETUP_EXCEPT] = self.op_SETUP_EXCEPT
        self.dispatch_table[Opcode.POP_EXCEPT] = self.op_POP_EXCEPT
        self.dispatch_table[Opcode.THROW] = self.op_THROW
        self.dispatch_table[Opcode.RETHROW] = self.op_RETHROW
        self.dispatch_table[Opcode.SETUP_FINALLY] = self.op_SETUP_FINALLY
        self.dispatch_table[Opcode.EXEC_FINALLY] = self.op_EXEC_FINALLY

    def build_stacktrace(self):
        trace = []
        for frame in reversed(self.vm.call_stack.frames):
            ip = frame[0]
            is_comp = frame[1]
            trace.append({'action': 'component' if is_comp else 'function', 'ip': ip, 'line': -1})
        return trace

    def _throw_exception(self, exc):
        from runtime.vm.exceptions import AayuException, InternalException
        if not isinstance(exc, AayuException):
            exc = InternalException(str(exc))
        exc.stacktrace = self.build_stacktrace()
        handled = False
        if hasattr(self.vm, 'block_stack'):
            while len(self.vm.block_stack) > 0:
                block = self.vm.block_stack.pop()
                if block['type'] == 'TRY':
                    while self.vm.value_stack.depth() > block['stack_depth']:
                        self.vm.value_stack.pop()
                    self.vm.value_stack.push(exc)
                    self.vm.registers.ip = block['handler_ip']
                    handled = True
                    break
        if not handled:
            mode = getattr(self.vm.config, 'mode', 'SERVER')
            if mode == 'CLI':
                print(f'[AAYU PANIC] {exc.exc_type}: {exc.message}')
                import sys
                sys.exit(1)
            else:
                raise exc

    def run(self):
        self.vm.profiler.start_time = time.time()
        while True:
            if self.vm.config.timeout_ms > 0:
                elapsed = (time.time() - self.vm.profiler.start_time) * 1000
                if elapsed > self.vm.config.timeout_ms:
                    print(f'Warning: Loop running for {self.vm.config.timeout_ms}ms. Terminating.')
                    break
            if self.vm.config.debug_mode and self.vm.config.enable_assertions:
                self._run_assertions()
            self.vm.debugger.check_breakpoint()
            opcode = self.vm.decoder.fetch8(self.vm.registers.ip)
            if self.vm.config.debug_mode:
                print(f'[VM TRACE] IP={self.vm.registers.ip} Opcode={opcode:02X} depth={self.vm.call_stack.depth()}')
            self.vm.profiler.tick(len(self.vm.heap.allocator.pool.pool) * 64)
            handler = self.dispatch_table[opcode]
            if handler is None:
                self._throw_exception(KernelError(f'Unknown opcode 0x{opcode:02X} at IP {self.vm.registers.ip}'))
                break
            result = handler(opcode)
            if result is False:
                break
        self.vm.profiler.end_time = time.time()

    def _run_assertions(self):
        assert self.vm.value_stack.depth() >= 0, 'ASSERT Stack Underflow'
        assert self.vm.registers.ip >= 0, 'ASSERT Instruction Pointer'

    def op_HALT(self, opcode):
        return False

    def op_PUSH_CONST(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        val = self.vm.constant_pool[idx]
        self.vm.value_stack.push(val)
        return True

    def op_POP(self, opcode):
        self.vm.registers.ip += 3
        self.vm.value_stack.pop()
        return True

    def op_ADD(self, opcode):
        self.vm.registers.ip += 3
        b = self.vm.value_stack.pop()
        a = self.vm.value_stack.pop()
        if isinstance(a, str) or isinstance(b, str):
            self.vm.value_stack.push(str(a) + str(b))
        else:
            self.vm.value_stack.push(a + b)
        return True

    def op_SUB(self, opcode):
        self.vm.registers.ip += 3
        b = self.vm.value_stack.pop()
        a = self.vm.value_stack.pop()
        self.vm.value_stack.push(a - b)
        return True

    def op_MUL(self, opcode):
        self.vm.registers.ip += 3
        b = self.vm.value_stack.pop()
        a = self.vm.value_stack.pop()
        self.vm.value_stack.push(a * b)
        return True

    def op_DIV(self, opcode):
        self.vm.registers.ip += 3
        b = self.vm.value_stack.pop()
        a = self.vm.value_stack.pop()
        if b == 0:
            from runtime.vm.exceptions import RuntimeException
            self._throw_exception(RuntimeException('Division by zero', code='AYU-1001'))
            return True
        self.vm.value_stack.push(a / b)
        return True

    def op_CMP_EQ(self, opcode):
        self.vm.registers.ip += 3
        b = self.vm.value_stack.pop()
        a = self.vm.value_stack.pop()
        print(f'[VM DEBUG] CMP_EQ: {repr(a)} == {repr(b)}')
        self.vm.value_stack.push(a == b)
        return True

    def op_CMP_NEQ(self, opcode):
        self.vm.registers.ip += 3
        b = self.vm.value_stack.pop()
        a = self.vm.value_stack.pop()
        self.vm.value_stack.push(a != b)
        return True

    def op_CMP_LT(self, opcode):
        self.vm.registers.ip += 3
        b = self.vm.value_stack.pop()
        a = self.vm.value_stack.pop()
        self.vm.value_stack.push(a < b)
        return True

    def op_CMP_GT(self, opcode):
        self.vm.registers.ip += 3
        b = self.vm.value_stack.pop()
        a = self.vm.value_stack.pop()
        self.vm.value_stack.push(a > b)
        return True

    def op_CMP_LTE(self, opcode):
        self.vm.registers.ip += 3
        b = self.vm.value_stack.pop()
        a = self.vm.value_stack.pop()
        self.vm.value_stack.push(a <= b)
        return True

    def op_CMP_GTE(self, opcode):
        self.vm.registers.ip += 3
        b = self.vm.value_stack.pop()
        a = self.vm.value_stack.pop()
        self.vm.value_stack.push(a >= b)
        return True

    def op_STORE_STATE(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        name = self.vm.constant_pool[idx]
        val = self.vm.value_stack.pop()
        self.vm.update_state(name, val)
        return True

    def op_LOAD_STATE(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        name = self.vm.constant_pool[idx]
        val = None
        found = False
        for scope in reversed(self.vm.state_scopes):
            if name in scope:
                val = scope[name]
                found = True
                break
        if not found:
            if hasattr(self.vm, 'action_addresses') and name in self.vm.action_addresses:
                val = name
            else:
                val = None
        self.vm.value_stack.push(val)
        return True

    def op_INIT_STATE(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        name = self.vm.constant_pool[idx]
        val = self.vm.value_stack.pop()
        if not self.vm.state_scopes:
            raise KernelError(f'state_scopes is empty at IP {self.vm.registers.ip - 3}')
        if name not in self.vm.state_scopes[-1]:
            self.vm.state_scopes[-1][name] = val
        return True

    def op_CALL_COMPONENT(self, opcode):
        target = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        base_depth = self.vm.value_stack.depth()
        self.vm.call_stack.push((self.vm.registers.ip + 3, True, 0, 1, base_depth))
        props = self.vm.value_stack.pop()
        scope = {}
        if isinstance(props, dict):
            for k, v in props.items():
                scope[k] = v
        if hasattr(self.vm, 'state_scopes'):
            self.vm.state_scopes.append(scope)
        self.vm.registers.ip = target
        return True

    def op_PREPARE_CALL(self, opcode):
        self.vm.registers.ip += 3
        return True

    def op_CALL(self, opcode):
        if self.vm.registers.ip >= 3 and self.vm.decoder.fetch8(self.vm.registers.ip - 3) == Opcode.PREPARE_CALL:
            args = self.vm.decoder.fetch8(self.vm.registers.ip - 2)
            returns = self.vm.decoder.fetch8(self.vm.registers.ip - 1)
        else:
            self.vm.raise_exception('Runtime security violation: Naked CALL without PREPARE_CALL')
            return False
        target = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        base_depth = self.vm.value_stack.depth()
        self.vm.call_stack.push((self.vm.registers.ip + 3, False, returns, args, base_depth))
        if hasattr(self.vm, 'state_scopes'):
            self.vm.state_scopes.append({})
        self.vm.registers.ip = target
        return True

    def op_MARK_BLOCK_START(self, opcode):
        self.vm.registers.ip += 3
        self.node_stack.append('$BLOCK_START')
        return True

    def op_CREATE_CLOSURE(self, opcode):
        num_args = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        action_name = self.vm.value_stack.pop()
        args = []
        for _ in range(num_args):
            args.insert(0, self.vm.value_stack.pop())
        closure = {'name': action_name, 'args': args}
        self.vm.value_stack.push(closure)
        return True

    def op_BUILD_WIDGET(self, opcode):
        operand = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        widget_type = operand >> 8 & 255
        dynamic_prop_count = operand & 255
        props = self.vm.value_stack.pop()
        dynamic_values = []
        for _ in range(dynamic_prop_count):
            dynamic_values.append(self.vm.value_stack.pop())
        if isinstance(props, dict):
            props = props.copy()
            stack_keys = [k for k, v in props.items() if v == '$STACK']
            if len(stack_keys) == dynamic_prop_count:
                for key in reversed(stack_keys):
                    props[key] = dynamic_values.pop(0)
        elif isinstance(props, str) and props == '__DYNAMIC__':
            if dynamic_prop_count == 1:
                props = dynamic_values.pop(0)
        from compiler.bytecode.encoder import WIDGET_TYPES
        widget_name = next((k for k, v in WIDGET_TYPES.items() if v == widget_type), 'UNKNOWN')
        is_block = widget_name.lower() in ['container', 'row', 'column', 'card', 'stack', 'center', 'expanded', 'padding', 'scrollview', 'grid', 'appbar', 'navigationbar', 'list', 'form', 'dialog', 'drawer', 'snackbar', 'tabbar', 'scaffold', 'page', 'component']
        children = []
        if is_block:
            while self.node_stack and self.node_stack[-1] != '$BLOCK_START':
                children.insert(0, self.node_stack.pop())
            if self.node_stack and self.node_stack[-1] == '$BLOCK_START':
                self.node_stack.pop()
        node = RenderNode(widget_name, props=props)
        node.children = children
        if widget_name == 'PAGE':
            self.render_tree.root = node
        else:
            self.node_stack.append(node)
        return True

    def op_PRINT(self, opcode):
        self.vm.registers.ip += 3
        val = self.vm.value_stack.pop()
        print(val)
        return True

    def op_JMP_IF_FALSE(self, opcode):
        target = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        cond = self.vm.value_stack.pop()
        if not cond:
            self.vm.registers.ip = target
        else:
            self.vm.registers.ip += 3
        return True

    def op_JMP(self, opcode):
        target = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip = target
        return True

    def op_CREATE_MODEL(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        model_name = self.vm.value_stack.pop()
        payload = self.vm.constant_pool[idx]
        if isinstance(payload, dict) and 'fields' in payload:
            self.vm.database.create_model(model_name, payload.get('fields', []), payload.get('decorators', []))
        else:
            self.vm.database.create_model(model_name, payload)
        return True

    def op_REGISTER_ROUTE(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        path = self.vm.value_stack.pop()
        methods_meta = self.vm.constant_pool[idx]
        self.vm.api_router.register_route(path, methods_meta)
        self.vm.api_router.start()
        return True

    def op_CHECK_AUTH(self, opcode):
        self.vm.registers.ip += 3
        token = None
        if self.vm.state_scopes:
            for scope in reversed(self.vm.state_scopes):
                if 'authToken' in scope:
                    token = scope['authToken']
                    break
        if not token:
            token = self.vm.state.get('authToken')
        if not token:
            from runtime.vm.exceptions import AuthenticationException
            self._throw_exception(AuthenticationException('Missing auth token', code='AYU-2001'))
            return True
        from runtime.stdlib.modules.auth_lib import verify_jwt
        payload = verify_jwt(token)
        if not payload:
            from runtime.vm.exceptions import AuthenticationException
            self._throw_exception(AuthenticationException('Invalid or expired auth token', code='AYU-2001'))
            return True
        if self.vm.state_scopes:
            self.vm.state_scopes[-1]['req_user'] = payload
        else:
            self.vm.state['req_user'] = payload
        return True

    def op_RETURN_VALUE(self, opcode):
        if opcode == Opcode.RETURN_VALUE:
            self.vm.registers.ip += 3
        if self.vm.call_stack.depth() > 0:
            ret_ip, is_comp, expected_returns, args, base_depth = self.vm.call_stack.pop()
            if opcode == Opcode.RETURN_VALUE:
                if expected_returns is not None and expected_returns != 1:
                    self.vm.raise_exception(f'Runtime ABI violation: RETURN_VALUE expected 1 return but action was declared with {expected_returns} returns')
                    return False
                expected_exit_depth = base_depth - args + 1
            else:
                if expected_returns is not None and expected_returns != 0:
                    self.vm.raise_exception(f'Runtime ABI violation: RET expected 0 returns but action was declared with {expected_returns} returns')
                    return False
                expected_exit_depth = base_depth - args
            current_depth = self.vm.value_stack.depth()
            if current_depth != expected_exit_depth:
                self.vm.raise_exception(f'Runtime ABI violation: Stack depth mismatch on return. Expected {expected_exit_depth}, got {current_depth}')
                return False
            if hasattr(self.vm, 'state_scopes') and len(self.vm.state_scopes) > 1:
                self.vm.state_scopes.pop()
            if is_comp:
                if self.node_stack:
                    self.node_stack.pop()
            self.vm.registers.ip = ret_ip
        else:
            return False
        return True

    def op_RET(self, opcode):
        if opcode == Opcode.RETURN_VALUE:
            self.vm.registers.ip += 3
        if self.vm.call_stack.depth() > 0:
            ret_ip, is_comp, expected_returns, args, base_depth = self.vm.call_stack.pop()
            if opcode == Opcode.RETURN_VALUE:
                if expected_returns is not None and expected_returns != 1:
                    self.vm.raise_exception(f'Runtime ABI violation: RETURN_VALUE expected 1 return but action was declared with {expected_returns} returns')
                    return False
                expected_exit_depth = base_depth - args + 1
            else:
                if expected_returns is not None and expected_returns != 0:
                    self.vm.raise_exception(f'Runtime ABI violation: RET expected 0 returns but action was declared with {expected_returns} returns')
                    return False
                expected_exit_depth = base_depth - args
            current_depth = self.vm.value_stack.depth()
            if current_depth != expected_exit_depth:
                self.vm.raise_exception(f'Runtime ABI violation: Stack depth mismatch on return. Expected {expected_exit_depth}, got {current_depth}')
                return False
            if hasattr(self.vm, 'state_scopes') and len(self.vm.state_scopes) > 1:
                self.vm.state_scopes.pop()
            if is_comp:
                if self.node_stack:
                    self.node_stack.pop()
            self.vm.registers.ip = ret_ip
        else:
            return False
        return True

    def op_DECLARE_THEME(self, opcode):
        self.vm.registers.ip += 3
        props = self.vm.value_stack.pop()
        name = self.vm.value_stack.pop()
        from runtime.ui.theme import ThemeManager
        ThemeManager.instance().register_theme(name, props)
        return True

    def op_SET_THEME(self, opcode):
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
        return True

    def op_NAVIGATE(self, opcode):
        num_args = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        keys = self.vm.value_stack.pop()
        target = self.vm.value_stack.pop()
        params = {}
        if keys:
            for key in reversed(keys):
                params[key] = self.vm.value_stack.pop()
        self.vm.router.navigate(target, params)
        return True

    def op_BUILD_DICT(self, opcode):
        self.vm.registers.ip += 3
        keys = self.vm.value_stack.pop()
        d = {}
        if self.vm.config.debug_mode:
            print(f'[DEBUG BUILD_DICT] keys: {keys}, stack depth: {self.vm.value_stack.depth()}')
        for key in reversed(keys):
            try:
                d[key] = self.vm.value_stack.pop()
            except Exception as e:
                if self.vm.config.debug_mode:
                    print(f'[DEBUG BUILD_DICT ERROR] Failed popping for key: {key}. Current stack: {self.vm.value_stack.stack}')
                raise e
        self.vm.value_stack.push(d)
        return True

    def op_OP_ASYNC_CALL(self, opcode):
        num_args = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        func_name = self.vm.value_stack.pop()
        args = []
        for _ in range(num_args):
            args.insert(0, self.vm.value_stack.pop())
        stdlib = self.vm.stdlib
        if func_name in stdlib.registry.functions:
            func = stdlib.registry.functions[func_name]
            result = func(args, self.vm)
            self.vm.value_stack.push(result)
        elif isinstance(func_name, str) and (external := stdlib.registry.lookup_external(func_name)):
            provider, func = external
            if provider not in {'native', 'python', 'rust', 'js'}:
                raise RuntimeError(f"External provider '{provider}' for '{func_name}' is not executable yet")
            self.vm.value_stack.push(func(args, self.vm))
        elif isinstance(func_name, str) and '.' in func_name:
            parts = func_name.split('.')
            target_name = parts[0]
            method_name = parts[1]
            target = None
            for scope in reversed(self.vm.state_scopes):
                if target_name in scope:
                    target = scope[target_name]
                    break
            if target is not None:
                dispatch_name = f'__method_{method_name}'
                args.insert(0, target)
                if dispatch_name in stdlib.registry.functions:
                    func = stdlib.registry.functions[dispatch_name]
                    result = func(args, self.vm)
                    self.vm.value_stack.push(result)
                else:
                    print(f'[VM Warning] Unresolved native method call: {func_name}')
                    self.vm.value_stack.push(None)
            else:
                print(f'[VM Warning] Unresolved target for method call: {func_name}')
                self.vm.value_stack.push(None)
        else:
            print(f'[VM Warning] Unresolved native function call: {func_name}')
            self.vm.value_stack.push(None)
        return True

    def op_SET_BINDING(self, opcode):
        self.vm.registers.ip += 3
        target = self.vm.value_stack.pop()
        self.node_stack.append(RenderNode('BINDING', props={'target': target}))
        return True

    def op_DECLARE_VALIDATION(self, opcode):
        self.vm.registers.ip += 3
        fields = self.vm.value_stack.pop()
        self.node_stack.append(RenderNode('VALIDATION', props={'fields': fields}))
        return True

    def op_SET_ANIMATION(self, opcode):
        self.vm.registers.ip += 3
        keys = self.vm.value_stack.pop()
        anim_props = {}
        for key in reversed(keys):
            anim_props[key] = self.vm.value_stack.pop()
        self.node_stack.append(RenderNode('ANIMATION', props={'props': anim_props}))
        return True

    def op_DECLARE_LIFECYCLE(self, opcode):
        offset = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        hook = self.vm.value_stack.pop()
        if self.vm.state_scopes:
            self.vm.state_scopes[-1][f'__lifecycle_{hook}__'] = offset
        return True

    def op_CREATE_ARRAY(self, opcode):
        count = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        elements = []
        for _ in range(count):
            elements.insert(0, self.vm.value_stack.pop())
        self.vm.value_stack.push(elements)
        return True

    def op_GET_LENGTH(self, opcode):
        self.vm.registers.ip += 3
        val = self.vm.value_stack.pop()
        if isinstance(val, (list, str, dict)):
            self.vm.value_stack.push(len(val))
        else:
            self.vm.value_stack.push(0)
        return True

    def op_LOAD_SUBSCR(self, opcode):
        self.vm.registers.ip += 3
        index = self.vm.value_stack.pop()
        container = self.vm.value_stack.pop()
        try:
            val = container[index]
        except (IndexError, KeyError, TypeError):
            val = None
        self.vm.value_stack.push(val)
        return True

    def op_STORE_SUBSCR(self, opcode):
        self.vm.registers.ip += 3
        index = self.vm.value_stack.pop()
        container = self.vm.value_stack.pop()
        value = self.vm.value_stack.pop()
        try:
            container[index] = value
        except (IndexError, KeyError, TypeError):
            pass
        return True

    def op_SETUP_EXCEPT(self, opcode):
        offset = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        if not hasattr(self.vm, 'block_stack'):
            from runtime.vm.stack import Stack
            self.vm.block_stack = Stack(max_depth=64)
        self.vm.block_stack.append({'type': 'TRY', 'handler_ip': offset, 'stack_depth': self.vm.value_stack.depth()})
        return True

    def op_POP_EXCEPT(self, opcode):
        self.vm.registers.ip += 3
        if hasattr(self.vm, 'block_stack') and len(self.vm.block_stack) > 0:
            block = self.vm.block_stack.pop()
            if block['type'] != 'TRY':
                raise KernelError('POP_EXCEPT called but top block is not TRY')
        return True

    def op_THROW(self, opcode):
        self.vm.registers.ip += 3
        exc = self.vm.value_stack.pop()
        self._throw_exception(exc)
        return True

    def op_RETHROW(self, opcode):
        self.vm.registers.ip += 3
        exc = self.vm.value_stack.pop()
        self._throw_exception(exc)
        return True

    def op_SETUP_FINALLY(self, opcode):
        offset = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        if not hasattr(self.vm, 'block_stack'):
            from runtime.vm.stack import Stack
            self.vm.block_stack = Stack(max_depth=64)
        self.vm.block_stack.append({'type': 'FINALLY', 'handler_ip': offset, 'stack_depth': self.vm.value_stack.depth()})
        return True

    def op_EXEC_FINALLY(self, opcode):
        self.vm.registers.ip += 3
        if hasattr(self.vm, 'block_stack') and len(self.vm.block_stack) > 0:
            block = self.vm.block_stack.pop()
            if block['type'] != 'FINALLY':
                pass
        return True
    def op_DB_INSERT(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        info = self.vm.constant_pool[idx]
        model_name = info["model"]
        fields_count = info["fields_count"]
        fields = {}
        for _ in range(fields_count):
            key = self.vm.value_stack.pop()
            val = self.vm.value_stack.pop()
            fields[key] = val
        import sqlite3
        try:
            conn = sqlite3.connect("aayu_db.sqlite")
            c = conn.cursor()
            cols = ", ".join(fields.keys())
            placeholders = ", ".join(["?"] * len(fields))
            vals = tuple(fields.values())
            c.execute(f"CREATE TABLE IF NOT EXISTS {model_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {cols})")
            c.execute(f"INSERT INTO {model_name} ({cols}) VALUES ({placeholders})", vals)
            conn.commit()
            conn.close()
            print(f"[DB] Inserted into {model_name}: {fields}")
        except Exception as e:
            print(f"[DB ERROR] Insert failed: {e}")
        return True

    def op_DB_FIND(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        model_name = self.vm.constant_pool[idx]
        import sqlite3
        try:
            conn = sqlite3.connect("aayu_db.sqlite")
            c = conn.cursor()
            c.execute(f"SELECT * FROM {model_name}")
            rows = c.fetchall()
            conn.close()
            self.vm.value_stack.push(rows)
            print(f"[DB] Found {len(rows)} records in {model_name}")
        except Exception as e:
            self.vm.value_stack.push([])
        return True

    def op_RESPOND(self, opcode):
        self.vm.registers.ip += 3
        val = self.vm.value_stack.pop()
        print(f"[HTTP RESPONSE] {val}")
        return True
