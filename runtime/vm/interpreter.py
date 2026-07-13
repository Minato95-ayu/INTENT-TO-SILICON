import time
from runtime.vm.instructions import Opcode
from runtime.vm.exceptions import KernelError
from runtime.vm.result import ResultStatus

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
