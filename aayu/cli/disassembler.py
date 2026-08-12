import sys
import struct
from pathlib import Path
from aayu.runtime.vm.instructions import Opcode
from aayu.compiler.backend.bytecode.aybc import TypeTag, MAGIC_BYTES

class Disassembler:
    """Parses and prints a human-readable assembly format from AYBC binary."""
    def __init__(self, binary: bytes):
        self.binary = binary
        self.offset = 0
        
        self.constants = []
        self.functions = []
        self.bytecode = b""

    def read(self, fmt: str):
        size = struct.calcsize(fmt)
        if self.offset + size > len(self.binary):
            raise EOFError("Unexpected EOF while parsing AYBC.")
        val = struct.unpack_from(fmt, self.binary, self.offset)
        self.offset += size
        return val[0] if len(val) == 1 else val

    def disassemble(self) -> str:
        try:
            self.parse_header()
            self.parse_constants()
            self.parse_functions()
            self.bytecode = self.binary[self.offset:]
            return self.format_output()
        except Exception as e:
            return f"Failed to disassemble: {e}"

    def parse_header(self):
        magic = self.binary[self.offset:self.offset+4]
        self.offset += 4
        if magic != MAGIC_BYTES:
            raise ValueError(f"Invalid magic bytes. Expected AYBC, got {magic}")
            
        self.version = self.read('<H')
        self.flags = self.read('<H')
        self.const_count = self.read('<I')
        self.func_count = self.read('<I')

    def parse_constants(self):
        for _ in range(self.const_count):
            tag = self.binary[self.offset]
            self.offset += 1
            if tag == TypeTag.INTEGER:
                val = self.read('<q')
                self.constants.append(val)
            elif tag == TypeTag.FLOAT:
                val = self.read('<d')
                self.constants.append(val)
            elif tag == TypeTag.BOOLEAN:
                val = self.binary[self.offset]
                self.offset += 1
                self.constants.append(bool(val))
            elif tag == TypeTag.NULL:
                self.constants.append(None)
            elif tag == TypeTag.STRING:
                length = self.read('<I')
                val = self.binary[self.offset:self.offset+length].decode('utf-8')
                self.offset += length
                self.constants.append(val)
            else:
                raise ValueError(f"Unknown TypeTag {tag}")

    def parse_functions(self):
        for _ in range(self.func_count):
            name_idx = self.read('<I')
            locals_count = self.read('<I')
            param_count = self.read('<I')
            max_stack = self.read('<I')
            bytecode_offset = self.read('<I')
            bytecode_length = self.read('<I')
            
            name = self.constants[name_idx]
            self.functions.append({
                "name": name,
                "locals": locals_count,
                "params": param_count,
                "max_stack": max_stack,
                "offset": bytecode_offset,
                "length": bytecode_length
            })

    def format_output(self) -> str:
        out = []
        out.append("=== AAYU BYTECODE DISASSEMBLY ===")
        out.append(f"Version: {self.version}")
        out.append(f"Flags: {self.flags}")
        out.append("")
        
        out.append("--- Constant Pool ---")
        for i, const in enumerate(self.constants):
            out.append(f"[{i:04}] {repr(const)}")
        out.append("")
        
        out.append("--- Functions ---")
        for func in self.functions:
            out.append(f"Function: {func['name']}")
            out.append(f"  Locals: {func['locals']}")
            out.append(f"  Max Stack: {func['max_stack']}")
            out.append(f"  Code Offset: {func['offset']}")
            out.append(f"  Code Length: {func['length']}")
            out.append("  Bytecode:")
            
            start = func['offset']
            end = start + func['length']
            ip = start
            
            while ip < end:
                if ip >= len(self.bytecode):
                    break
                    
                opcode = self.bytecode[ip]
                from aayu.runtime.vm.instructions import opcode_to_str
                op_name = opcode_to_str(opcode)
                
                # Opcodes take 3 bytes
                arg_bytes = self.bytecode[ip+1:ip+3]
                if len(arg_bytes) == 2:
                    arg_val = struct.unpack('>H', arg_bytes)[0]
                else:
                    arg_val = 0
                
                # Format instruction
                instr_str = f"    {ip:04d} {op_name}"
                
                if opcode == Opcode.PUSH_CONST:
                    const_val = self.constants[arg_val] if arg_val < len(self.constants) else "<invalid>"
                    instr_str += f" {arg_val} ({repr(const_val)})"
                elif opcode in (Opcode.LOAD_LOCAL, Opcode.STORE_LOCAL):
                    instr_str += f" slot_{arg_val}"
                elif opcode in (Opcode.JMP, Opcode.JMP_IF_FALSE):
                    instr_str += f" {arg_val:04d}"
                
                out.append(instr_str)
                ip += 3
            out.append("")
            
        return "\n".join(out)

def main():
    if len(sys.argv) < 2:
        print("Usage: aayu dis <file.aybc>")
        sys.exit(1)
        
    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"File not found: {filepath}")
        sys.exit(1)
        
    with open(filepath, "rb") as f:
        binary = f.read()
        
    dis = Disassembler(binary)
    print(dis.disassemble())

if __name__ == "__main__":
    main()
