import time
from runtime.vm.instructions import Opcode
from runtime.vm.exceptions import KernelError
from runtime.vm.result import ResultStatus

# Widget type names for BUILD_WIDGET display
WIDGET_TYPE_NAMES = {
    0: "TEXT",
    1: "BUTTON",
    2: "CONTAINER",
    3: "IMAGE",
    4: "ROW",
    5: "COLUMN",
    6: "CARD",
    7: "INPUT",
    8: "PAGE",
}

class Interpreter:
    """Core bytecode dispatch loop.
    
    All instructions are fixed-width: 3 bytes.
        [OPCODE: 1 byte] [OPERAND: 2 bytes big-endian]
    IP always advances by 3 per instruction (except jumps).
    """
    INSTRUCTION_WIDTH = 3

    def __init__(self, vm):
        self.vm = vm
        self.output_lines = []  # Collected output for console rendering
        
    def run(self):
        self.vm.profiler.start_time = time.time()
        self.output_lines = []
        
        while True:
            # Infinite loop timeout check (dev mode)
            if self.vm.config.timeout_ms > 0:
                elapsed = (time.time() - self.vm.profiler.start_time) * 1000
                if elapsed > self.vm.config.timeout_ms:
                    print(f"Warning: Loop running for {self.vm.config.timeout_ms}ms. Terminating.")
                    break
                    
            if self.vm.config.debug_mode and self.vm.config.enable_assertions:
                self._run_assertions()
                
            self.vm.debugger.check_hook(self.vm.registers.ip)
            
            opcode = self.vm.decoder.fetch8(self.vm.registers.ip)
            
            # Profiler tick
            self.vm.profiler.tick(len(self.vm.heap.allocator.pool.pool) * 64)
            
            if opcode == Opcode.HALT:
                break
                
            elif opcode == Opcode.PUSH_CONST:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                val = self.vm.constant_pool[idx]
                self.vm.value_stack.push(val)
                
            elif opcode == Opcode.POP:
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                self.vm.value_stack.pop()
                
            elif opcode == Opcode.DUP:
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                val = self.vm.value_stack.peek()
                self.vm.value_stack.push(val)
                
            elif opcode == Opcode.ADD:
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a + b)
                
            elif opcode == Opcode.SUB:
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a - b)

            elif opcode == Opcode.MUL:
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a * b)

            elif opcode == Opcode.DIV:
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                self.vm.value_stack.push(a / b)
                
            elif opcode == Opcode.STORE_STATE:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                name = self.vm.constant_pool[idx]
                val = self.vm.value_stack.pop()
                self.vm.state[name] = val
                
            elif opcode == Opcode.LOAD_STATE:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                name = self.vm.constant_pool[idx]
                val = self.vm.state.get(name, None)
                self.vm.value_stack.push(val)
                
            elif opcode == Opcode.JMP_IF_FALSE:
                target = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                cond = self.vm.value_stack.pop()
                if not cond:
                    self.vm.registers.ip = target
                else:
                    self.vm.registers.ip += self.INSTRUCTION_WIDTH
                    
            elif opcode == Opcode.JMP:
                target = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip = target

            elif opcode == Opcode.CALL:
                target = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                # Push return address
                self.vm.call_stack.push(self.vm.registers.ip + self.INSTRUCTION_WIDTH)
                self.vm.registers.ip = target

            elif opcode == Opcode.RET:
                if self.vm.call_stack.depth() > 0:
                    return_addr = self.vm.call_stack.pop()
                    self.vm.registers.ip = return_addr
                else:
                    # No return address — behave like HALT
                    break

            elif opcode == Opcode.PRINT:
                # Pop value from stack and print to stdout
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                val = self.vm.value_stack.pop()
                output = str(val) if val is not None else ""
                print(output)
                self.output_lines.append(output)

            elif opcode == Opcode.BUILD_WIDGET:
                # Pop content from stack, operand = widget type ID
                widget_type_id = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                content = self.vm.value_stack.pop()
                
                widget_name = WIDGET_TYPE_NAMES.get(widget_type_id, "UNKNOWN")
                
                # Console renderer: print widget content
                if widget_name == "TEXT":
                    output = str(content) if content else ""
                    if output:
                        print(output)
                        self.output_lines.append(output)
                elif widget_name == "BUTTON":
                    output = f"[{content}]"
                    print(output)
                    self.output_lines.append(output)
                elif widget_name == "PAGE":
                    output = f"=== {content} ==="
                    print(output)
                    self.output_lines.append(output)
                else:
                    # Container, Row, Column, etc. — structural, no console output
                    pass
                
            elif opcode == Opcode.DISPATCH:
                # Kernel/Plugin invocation
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                try:
                    result = self.vm.kernel_dispatch()
                    if result.status == ResultStatus.ERROR:
                        raise KernelError(result.error_message)
                except KernelError as e:
                    print(f"Kernel caught exception: {e}")
                    self.vm.value_stack.push(None)
                    
            else:
                # Unknown opcode — skip
                self.vm.registers.ip += self.INSTRUCTION_WIDTH
                
        self.vm.profiler.end_time = time.time()
        
    def _run_assertions(self):
        assert self.vm.value_stack.depth() >= 0, "ASSERT Stack Underflow"
        assert self.vm.registers.ip >= 0, "ASSERT Instruction Pointer"
