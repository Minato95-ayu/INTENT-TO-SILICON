from aayu.runtime.vm.frame import CallFrame
from aayu.runtime.vm.exceptions import StackOverflowError

class CallStack:
    """
    Manages CallFrames with depth protection.
    """
    def __init__(self, max_depth: int = 4096):
        self.frames = []
        self.max_depth = max_depth
        
    def push(self, frame: CallFrame):
        if len(self.frames) >= self.max_depth:
            raise StackOverflowError(self.max_depth)
        self.frames.append(frame)
        
    def pop(self) -> CallFrame:
        if not self.frames:
            return None
        return self.frames.pop()
        
    def current(self) -> CallFrame:
        if not self.frames:
            return None
        return self.frames[-1]
        
    def depth(self) -> int:
        return len(self.frames)

class ValueStack:
    """Operand stack for the VM with O(1) array allocation."""
    def __init__(self, max_depth: int = 16384):
        self.max_depth = max_depth
        self.stack = [None] * max_depth
        self.sp = 0
        
    def push(self, val):
        if self.sp >= self.max_depth:
            raise RuntimeError("ValueStack overflow")
        self.stack[self.sp] = val
        self.sp += 1
        
    def pop(self):
        if self.sp == 0:
            raise RuntimeError("ValueStack underflow")
        self.sp -= 1
        return self.stack[self.sp]
        
    def peek(self):
        if self.sp == 0:
            return None
        return self.stack[self.sp - 1]
        
    def depth(self):
        return self.sp
