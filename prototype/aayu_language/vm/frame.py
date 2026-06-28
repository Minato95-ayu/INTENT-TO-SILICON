from ir import Bytecode
from typing import List, Dict, Any
from vm.stack import Stack

class CallFrame:
    def __init__(self, bytecode: Bytecode, locals_dict: dict, frame_name: str = "main"):
        self.bytecode = bytecode
        self.locals = locals_dict
        self.ip = 0
        self.stack = Stack()
        self.return_ip = -1
        self.function = None
        self.frame_name = frame_name
        self.source_file = getattr(bytecode, 'file', '')
