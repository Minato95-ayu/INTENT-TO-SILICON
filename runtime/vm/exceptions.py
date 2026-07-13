class VMError(Exception):
    """Base class for all VM errors."""
    pass

class InvalidBytecodeError(VMError):
    """Raised by Validator when bytecode is malformed."""
    def __init__(self, message, offset=-1):
        super().__init__(f"InvalidBytecodeError at offset {offset}: {message}")
        self.offset = offset

class StackOverflowError(VMError):
    """Raised when call stack exceeds MAX_CALL_DEPTH."""
    def __init__(self, depth, file="main.aayu", line=-1):
        super().__init__(f"StackOverflowError: Maximum call depth exceeded.\nCall depth: {depth}\nFile: {file}\nLine: {line}")
        self.depth = depth

class KernelError(VMError):
    """Raised when a kernel/plugin throws an unrecoverable error."""
    pass
