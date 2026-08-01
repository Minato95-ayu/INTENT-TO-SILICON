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
    """Operand stack for the VM."""
    def __init__(self):
        self.stack = []
        
    def push(self, val):
        self.stack.append(val)
        
    def pop(self):
        if not self.stack:
            raise RuntimeError("ValueStack underflow")
        return self.stack.pop()
        
    def peek(self):
        return self.stack[-1] if self.stack else None
        
    def depth(self):
        return len(self.stack)
