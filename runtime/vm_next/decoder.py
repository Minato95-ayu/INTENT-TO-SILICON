from runtime.vm_next.instructions import Opcode

class Decoder:
    """Decodes bytecode stream into instructions."""
    def __init__(self, bytecode, constant_pool):
        self.bytecode = bytecode
        self.constant_pool = constant_pool
        self.length = len(bytecode)
        
    def fetch8(self, ip: int) -> int:
        if ip >= self.length:
            return Opcode.HALT
        return self.bytecode[ip]
        
    def fetch16(self, ip: int) -> int:
        if ip + 1 >= self.length:
            return 0
        return (self.bytecode[ip] << 8) | self.bytecode[ip + 1]
