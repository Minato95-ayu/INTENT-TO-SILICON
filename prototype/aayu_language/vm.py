from ir import Opcode, Bytecode
from errors import AAYURuntimeError

class CallFrame:
    def __init__(self, bytecode: Bytecode, locals_dict: dict, frame_name: str = "main"):
        self.bytecode = bytecode
        self.locals = locals_dict
        self.ip = 0
        self.stack = []
        self.frame_name = frame_name

class VirtualMachine:
    def __init__(self):
        self.frames = []
        self.globals = {}
        self.output = []
        self.instruction_count = 0

    def run(self, bytecode: Bytecode):
        self.globals = {}
        self.output = []
        self.instruction_count = 0
        
        main_frame = CallFrame(bytecode, {}, "main")
        self.frames = [main_frame]
        
        while self.frames:
            self.instruction_count += 1
            current_frame = self.frames[-1]
            
            if current_frame.ip >= len(current_frame.bytecode.instructions):
                self.frames.pop()
                continue
                
            instruction = current_frame.bytecode.instructions[current_frame.ip]
            opcode = instruction.opcode
            operand = instruction.operand
            
            if opcode == Opcode.LOAD_CONST:
                val = current_frame.bytecode.constants[operand]
                current_frame.stack.append(val)
                
            elif opcode == Opcode.STORE_NAME:
                val = current_frame.stack.pop()
                name = current_frame.bytecode.names[operand]
                if len(self.frames) == 1:
                    self.globals[name] = val
                else:
                    current_frame.locals[name] = val
                    
            elif opcode == Opcode.LOAD_NAME:
                name = current_frame.bytecode.names[operand]
                if name in current_frame.locals:
                    current_frame.stack.append(current_frame.locals[name])
                elif name in self.globals:
                    current_frame.stack.append(self.globals[name])
                else:
                    raise AAYURuntimeError(f"Undefined variable '{name}'.", 1, f"Initialize the variable before using it.")
                    
            elif opcode == Opcode.POP:
                current_frame.stack.pop()
                    
            elif opcode == Opcode.ADD:
                right = current_frame.stack.pop()
                left = current_frame.stack.pop()
                current_frame.stack.append(left + right)
                
            elif opcode == Opcode.SUB:
                right = current_frame.stack.pop()
                left = current_frame.stack.pop()
                current_frame.stack.append(left - right)
                
            elif opcode == Opcode.MUL:
                right = current_frame.stack.pop()
                left = current_frame.stack.pop()
                current_frame.stack.append(left * right)
                
            elif opcode == Opcode.DIV:
                right = current_frame.stack.pop()
                left = current_frame.stack.pop()
                current_frame.stack.append(left / right)
                
            elif opcode == Opcode.EQUAL:
                right = current_frame.stack.pop()
                left = current_frame.stack.pop()
                current_frame.stack.append(left == right)
                
            elif opcode == Opcode.GREATER:
                right = current_frame.stack.pop()
                left = current_frame.stack.pop()
                current_frame.stack.append(left > right)
                
            elif opcode == Opcode.LESS:
                right = current_frame.stack.pop()
                left = current_frame.stack.pop()
                current_frame.stack.append(left < right)
                
            elif opcode == Opcode.NOT:
                val = current_frame.stack.pop()
                current_frame.stack.append(not val)
                
            elif opcode == Opcode.JUMP_FORWARD:
                current_frame.ip += operand
                continue
                
            elif opcode == Opcode.JUMP_IF_FALSE:
                condition = current_frame.stack.pop()
                if not condition:
                    current_frame.ip += operand
                    continue
                    
            elif opcode == Opcode.JUMP_BACKWARD:
                current_frame.ip -= operand
                continue
                
            elif opcode == Opcode.CALL_TASK:
                n_args = operand
                task_obj = current_frame.stack.pop()
                
                args = []
                for _ in range(n_args):
                    args.append(current_frame.stack.pop())
                args.reverse()
                
                if not isinstance(task_obj, Bytecode):
                    raise AAYURuntimeError(f"Object is not callable.", 1, "")
                    
                locals_dict = {}
                for param, val in zip(task_obj.parameters, args):
                    locals_dict[param] = val
                    
                new_frame = CallFrame(task_obj, locals_dict, task_obj.name)
                
                # Advance caller frame IP so it resumes AFTER the CALL_TASK instruction
                current_frame.ip += 1
                
                self.frames.append(new_frame)
                continue
                
            elif opcode == Opcode.RETURN:
                if current_frame.stack:
                    ret_val = current_frame.stack.pop()
                else:
                    ret_val = None
                    
                self.frames.pop()
                
                if self.frames:
                    self.frames[-1].stack.append(ret_val)
                continue
                
            elif opcode == Opcode.BUILD_LIST:
                current_frame.stack.append([])
                
            elif opcode == Opcode.BUILD_MAP:
                current_frame.stack.append({})
                
            elif opcode == Opcode.ADD_TO_LIST:
                list_obj = current_frame.stack.pop()
                item = current_frame.stack.pop()
                if not isinstance(list_obj, list):
                    raise AAYURuntimeError("Target of 'add' must be a list.", 1, "")
                list_obj.append(item)
                current_frame.stack.append(list_obj)
                
            elif opcode == Opcode.MAP_SET:
                map_obj = current_frame.stack.pop()
                key = current_frame.stack.pop()
                value = current_frame.stack.pop()
                if not isinstance(map_obj, dict):
                    raise AAYURuntimeError("Target of 'set' must be a map.", 1, "")
                map_obj[key] = value
                
            elif opcode == Opcode.GET_ITEM:
                coll = current_frame.stack.pop()
                key = current_frame.stack.pop()
                if isinstance(coll, list):
                    try:
                        idx = int(key)
                        current_frame.stack.append(coll[idx])
                    except (ValueError, TypeError):
                        raise AAYURuntimeError(f"List index must be an integer, got '{key}'.", 1, "")
                    except IndexError:
                        raise AAYURuntimeError(f"List index out of range: {key}.", 1, "")
                elif isinstance(coll, dict):
                    if key not in coll:
                        raise AAYURuntimeError(f"Key '{key}' not found in map.", 1, "")
                    current_frame.stack.append(coll[key])
                else:
                    raise AAYURuntimeError("Cannot read items from a non-collection object.", 1, "")

            elif opcode == Opcode.PRINT:
                val = current_frame.stack.pop()
                self.output.append(val)
                print(val)
                
            else:
                raise Exception(f"VM Error: Unimplemented opcode {opcode}")
                
            current_frame.ip += 1
