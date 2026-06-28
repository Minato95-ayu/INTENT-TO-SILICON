from vm.frame import CallFrame

def execute_load_const(vm, frame, operand):
    frame.stack.push(frame.bytecode.constants[operand])

def execute_load_var(vm, frame, operand):
    name = frame.bytecode.names[operand]
    if name in frame.locals:
        frame.stack.push(frame.locals[name])
    elif name in vm.memory.globals:
        frame.stack.push(vm.memory.globals[name])
    else:
        raise RuntimeError(f"Undefined variable '{name}'")

def execute_store_var(vm, frame, operand):
    name = frame.bytecode.names[operand]
    val = frame.stack.pop()
    # Scoping rule: if not global, it's local. Main frame acts as global scope.
    if frame.frame_name == "main" and name not in frame.locals:
        vm.memory.globals[name] = val
    else:
        frame.locals[name] = val

def execute_add(vm, frame, operand):
    r = frame.stack.pop()
    l = frame.stack.pop()
    frame.stack.push(l + r)

def execute_sub(vm, frame, operand):
    r = frame.stack.pop()
    l = frame.stack.pop()
    frame.stack.push(l - r)

def execute_mul(vm, frame, operand):
    r = frame.stack.pop()
    l = frame.stack.pop()
    frame.stack.push(l * r)

def execute_div(vm, frame, operand):
    r = frame.stack.pop()
    l = frame.stack.pop()
    frame.stack.push(l / r)

def execute_eq(vm, frame, operand):
    r = frame.stack.pop()
    l = frame.stack.pop()
    frame.stack.push(l == r)

def execute_lt(vm, frame, operand):
    r = frame.stack.pop()
    l = frame.stack.pop()
    frame.stack.push(l < r)

def execute_gt(vm, frame, operand):
    r = frame.stack.pop()
    l = frame.stack.pop()
    frame.stack.push(l > r)

def execute_jump(vm, frame, operand):
    frame.ip += operand

def execute_jump_if_false(vm, frame, operand):
    cond = frame.stack.pop()
    if not cond:
        frame.ip += operand
    else:
        frame.ip += 1

def execute_call(vm, frame, operand):
    n_args = operand
    args = []
    for _ in range(n_args):
        args.insert(0, frame.stack.pop())
        
    fn = frame.stack.pop()
    
    if isinstance(fn, str) and fn in vm.builtins:
        ret = vm.builtins[fn](vm, args)
        frame.stack.push(ret)
        frame.ip += 1
    elif hasattr(fn, 'instructions'):
        new_locals = {}
        for i, param_name in enumerate(fn.parameters):
            if i < len(args):
                new_locals[param_name] = args[i]
                
        new_frame = CallFrame(fn, new_locals, frame_name=fn.name)
        new_frame.function = fn
        new_frame.return_ip = frame.ip + 1
        
        vm.frames.append(new_frame)
        vm.current_frame = new_frame
    else:
        raise RuntimeError(f"Cannot call non-function object: {fn}")

def execute_return(vm, frame, operand):
    val = None
    if not frame.stack.is_empty():
        val = frame.stack.pop()
        
    vm.frames.pop()
    if vm.frames:
        vm.current_frame = vm.frames[-1]
        vm.current_frame.stack.push(val)
        vm.current_frame.ip = frame.return_ip
    else:
        vm.return_value = val
        vm.current_frame = None
