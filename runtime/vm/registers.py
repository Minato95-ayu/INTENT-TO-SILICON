class Registers:
    __slots__ = ['acc', 'flags', 'fp', 'ip', 'sp']
    '\n    Core VM Registers.\n    IP: Instruction Pointer\n    SP: Stack Pointer\n    FP: Frame Pointer\n    ACC: Accumulator (for math/logic)\n    FLAGS: Status Flags (Zero, Sign, Overflow, etc.)\n    '

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