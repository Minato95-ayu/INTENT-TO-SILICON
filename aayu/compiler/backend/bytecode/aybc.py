"""
AYBC (AAYU Bytecode) Binary Format Specification
"""

import struct
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Union, Any

class TypeTag(IntEnum):
    INTEGER = 0x01
    FLOAT = 0x02
    STRING = 0x03
    BOOLEAN = 0x04
    NULL = 0x05

MAGIC_BYTES = b'AYBC'
VERSION = 1
FLAGS = 0

@dataclass
class FunctionMetadata:
    name_index: int      # Index into constant pool for the string name
    locals_count: int    # Number of local variable slots
    parameter_count: int # Number of parameters
    max_stack: int       # Maximum stack depth required
    bytecode_offset: int # Byte offset from start of bytecode section
    bytecode_length: int # Length of the bytecode for this function
    line_numbers_offset: int = 0
    line_numbers_length: int = 0

class AYBCFile:
    def __init__(self):
        self.constants: List[Any] = []
        self.functions: List[FunctionMetadata] = []
        self.bytecode: bytearray = bytearray()
        
    def add_constant(self, value: Any) -> int:
        if value in self.constants:
            return self.constants.index(value)
        self.constants.append(value)
        return len(self.constants) - 1
