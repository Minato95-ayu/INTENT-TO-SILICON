import sys
import os
sys.path.insert(0, r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\aayu_language")
sys.path.insert(0, r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype")
from lexer import Lexer
from parser import Parser
from compiler import AAYUCompiler
from vm import VirtualMachine, Frame
from opcode import Opcode

filepath = "D:\\intent-to-silicon-research\\INTENT-TO-SILICON\\test_func_ret.aayu"
with open(filepath, 'r', encoding='utf-8') as f:
    source = f.read()

lexer = Lexer(source)
parser = Parser(lexer.tokenize(), filename=filepath)
ast = parser.parse()
compiler = AAYUCompiler()
code_obj = compiler.compile(ast)

class TracingVirtualMachine(VirtualMachine):
    def run(self, code):
        frame = Frame(code)
        self.call_stack.append(frame)

        while self.call_stack:
            frame = self.call_stack[-1]

            if frame.ip >= len(frame.code.instructions):
                self.call_stack.pop()
                if self.call_stack:
                    self.call_stack[-1].stack.append(None)
                continue

            instruction = frame.code.instructions[frame.ip]
            print(f"IP: {frame.ip:04d} | Opcode: {instruction.opcode.name:<15} | Arg: {instruction.arg}")
            print(f"    Stack : {frame.stack}")
            print(f"    Locals: {frame.locals}")
            
            # Step the execution manually
            opcode = instruction.opcode
            arg = instruction.arg
            
            frame.ip += 1

            if opcode == Opcode.LOAD_CONST:
                frame.stack.append(arg)
            elif opcode == Opcode.STORE_VAR:
                frame.locals[arg] = frame.stack.pop()
            elif opcode == Opcode.LOAD_VAR:
                if arg in frame.locals:
                    frame.stack.append(frame.locals[arg])
                else:
                    raise RuntimeError(f"Variable '{arg}' is not defined.")
            elif opcode == Opcode.COMPARE_EQ:
                b = frame.stack.pop()
                a = frame.stack.pop()
                frame.stack.append(a == b)
            elif opcode == Opcode.JUMP_IF_FALSE:
                condition = frame.stack.pop()
                if not condition:
                    frame.ip = arg
            elif opcode == Opcode.JUMP_FORWARD:
                frame.ip = arg
            elif opcode == Opcode.CALL:
                func_name = arg['name']
                num_args = arg['num_args']
                
                args = []
                for _ in range(num_args):
                    args.insert(0, frame.stack.pop())
                
                if func_name == 'print':
                    # Built-in print
                    val = " ".join(map(str, args))
                    print(f"==> PRINT: {val}")
                    frame.stack.append(None)
                else:
                    if func_name in self.globals and isinstance(self.globals[func_name], CodeObject):
                        func_code = self.globals[func_name]
                        new_frame = Frame(func_code)
                        # The function should know its parameter names?
                        # Wait, we need to map arguments to parameter names...
                        self.call_stack.append(new_frame)
                        # We don't have parameter names in CodeObject! Wait...
                        # In AAYUCompiler we didn't store parameter names?
                    else:
                        raise RuntimeError(f"Function '{func_name}' is not defined.")
            elif opcode == Opcode.RETURN:
                if frame.stack:
                    ret_val = frame.stack.pop()
                else:
                    ret_val = None
                self.call_stack.pop()
                if self.call_stack:
                    self.call_stack[-1].stack.append(ret_val)
                else:
                    return ret_val
            else:
                raise RuntimeError(f"Unknown opcode: {opcode}")

print("=== TRACE ===")
vm = TracingVirtualMachine()
vm.globals = {"sum_nums": code_obj.instructions[0].arg} # manually add it for trace if needed, but it's not run yet...
vm.run(code_obj)
