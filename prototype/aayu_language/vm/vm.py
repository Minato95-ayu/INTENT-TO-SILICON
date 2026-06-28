from vm.frame import CallFrame
from vm.memory import Memory
from vm.builtins import BUILTINS
from vm.dispatcher import DISPATCH_TABLE
from errors import AAYURuntimeError

class VirtualMachine:
    def __init__(self, db_conn=None, db_cursor=None, db_lock=None):
        self.frames = []
        self.current_frame = None
        self.memory = Memory()
        self.builtins = BUILTINS
        self.output = []
        self.return_value = None
        self.instruction_count = 0
        
        # Original VM compatibility for db and stdlib
        if db_conn is not None:
            self.db_conn = db_conn
            self.db_cursor = db_cursor
        
    def _get_line_and_file(self, frame, ip):
        if ip < len(frame.bytecode.instructions):
            inst = frame.bytecode.instructions[ip]
            if getattr(inst, 'line', None) is not None:
                return inst.line, inst.file
            for idx in range(ip - 1, -1, -1):
                i = frame.bytecode.instructions[idx]
                if getattr(i, 'line', None) is not None:
                    return i.line, i.file
        return 1, frame.source_file
        
    def _raise_runtime_error(self, message, hint="", cls=AAYURuntimeError):
        if self.current_frame:
            line, _ = self._get_line_and_file(self.current_frame, self.current_frame.ip)
        else:
            line = 1
        raise cls(message, line, hint)

    def run(self, bytecode, initial_locals=None):
        if initial_locals is None:
            initial_locals = {}
            
        main_frame = CallFrame(bytecode, initial_locals, frame_name="main")
        self.frames.append(main_frame)
        self.current_frame = main_frame
        
        while self.current_frame is not None:
            if self.current_frame.ip >= len(self.current_frame.bytecode.instructions):
                # Auto-return if reached end of bytecode
                finished_frame = self.frames.pop()
                if self.frames:
                    self.current_frame = self.frames[-1]
                    self.current_frame.stack.push(None)
                    self.current_frame.ip = finished_frame.return_ip
                else:
                    self.current_frame = None
                continue
                
            instruction = self.current_frame.bytecode.instructions[self.current_frame.ip]
            self.instruction_count += 1
            
            opcode = instruction.opcode
            operand = instruction.operand
            
            handler = DISPATCH_TABLE.get(opcode)
            if handler:
                try:
                    handler(self, self.current_frame, operand)
                except Exception as e:
                    self._raise_runtime_error(str(e))
                    
                # Increment IP if the handler didn't change it via JUMP, CALL, or RETURN
                if opcode not in (opcode.JUMP, opcode.JUMP_IF_FALSE, opcode.CALL, opcode.RETURN):
                    self.current_frame.ip += 1
            else:
                self._raise_runtime_error(f"Unknown opcode: {opcode}")
                
        return self.return_value
