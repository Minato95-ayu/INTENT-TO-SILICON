from ir import Opcode, Bytecode
from errors import AAYURuntimeError

class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.variables = {}
        self.output = []
        self.ip = 0

    def run(self, bytecode: Bytecode):
        self.ip = 0
        self.stack = []
        
        while self.ip < len(bytecode.instructions):
            instruction = bytecode.instructions[self.ip]
            opcode = instruction.opcode
            operand = instruction.operand
            
            if opcode == Opcode.LOAD_CONST:
                val = bytecode.constants[operand]
                self.stack.append(val)
                
            elif opcode == Opcode.STORE_NAME:
                val = self.stack.pop()
                name = bytecode.names[operand]
                self.variables[name] = val
                
            elif opcode == Opcode.LOAD_NAME:
                name = bytecode.names[operand]
                if name not in self.variables:
                    raise AAYURuntimeError(f"Undefined variable '{name}'.", 1, f"Initialize the variable before using it.")
                self.stack.append(self.variables[name])
                
            elif opcode == Opcode.ADD:
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left + right)
                
            elif opcode == Opcode.SUB:
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left - right)
                
            elif opcode == Opcode.MUL:
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left * right)
                
            elif opcode == Opcode.DIV:
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left / right)
                
            elif opcode == Opcode.PRINT:
                val = self.stack.pop()
                self.output.append(val)
                print(val)
                
            elif opcode == Opcode.RETURN:
                break
                
            else:
                raise Exception(f"VM Error: Unimplemented opcode {opcode}")
                
            self.ip += 1
