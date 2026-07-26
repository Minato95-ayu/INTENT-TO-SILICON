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


class AayuException(VMError):
    """Structured Exception thrown by the AAYU VM."""
    def __init__(self, message, code="AYU-0000", file=None, action=None, line=None, column=None, stacktrace=None, cause=None, timestamp=None):
        self.exc_type = self.__class__.__name__
        self.message = message
        self.code = code
        self.file = file
        self.action = action
        self.line = line
        self.column = column
        self.stacktrace = stacktrace or []
        self.cause = cause
        import datetime
        self.timestamp = timestamp or datetime.datetime.utcnow().isoformat()
        super().__init__(f"{self.exc_type}: {self.message}")
        
    def to_dict(self):
        return {
            "type": self.exc_type,
            "message": self.message,
            "code": self.code,
            "file": self.file,
            "action": self.action,
            "line": self.line,
            "column": self.column,
            "stacktrace": self.stacktrace,
            "cause": self.cause,
            "timestamp": self.timestamp
        }

class RuntimeException(AayuException):
    def __init__(self, message, **kwargs):
        super().__init__(message, code=kwargs.pop('code', 'AYU-1001'), **kwargs)

class ValidationException(AayuException):
    def __init__(self, message, **kwargs):
        super().__init__(message, code=kwargs.pop('code', 'AYU-3001'), **kwargs)

class DatabaseException(AayuException):
    def __init__(self, message, **kwargs):
        super().__init__(message, code=kwargs.pop('code', 'AYU-4001'), **kwargs)

class AuthenticationException(AayuException):
    def __init__(self, message, **kwargs):
        super().__init__(message, code=kwargs.pop('code', 'AYU-2001'), **kwargs)

class AuthorizationException(AayuException):
    def __init__(self, message, **kwargs):
        super().__init__(message, code=kwargs.pop('code', 'AYU-2002'), **kwargs)

class CompilerException(AayuException):
    def __init__(self, message, **kwargs):
        super().__init__(message, code=kwargs.pop('code', 'AYU-5001'), **kwargs)

class SyntaxException(AayuException):
    def __init__(self, message, **kwargs):
        super().__init__(message, code=kwargs.pop('code', 'AYU-5002'), **kwargs)

class NetworkException(AayuException):
    def __init__(self, message, **kwargs):
        super().__init__(message, code=kwargs.pop('code', 'AYU-6001'), **kwargs)

class InternalException(AayuException):
    def __init__(self, message, **kwargs):
        super().__init__(message, code=kwargs.pop('code', 'AYU-9999'), **kwargs)
