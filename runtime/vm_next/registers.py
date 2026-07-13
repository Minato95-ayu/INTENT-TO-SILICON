class Registers:
    """
    Core VM Registers.
    IP: Instruction Pointer
    SP: Stack Pointer
    FP: Frame Pointer
    ACC: Accumulator (for math/logic)
    FLAGS: Status Flags (Zero, Sign, Overflow, etc.)
    """
    def __init__(self):
        self.ip = 0
        self.sp = 0
        self.fp = 0
        self.acc = 0
        self.flags = 0

    def reset(self):
        self.ip = 0
        self.sp = 0
        self.fp = 0
        self.acc = 0
        self.flags = 0
