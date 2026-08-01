"""
=============================================================================
FILE: exception.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from .base import RuntimeValue
from typing import Any, List


class ExceptionValue(RuntimeValue):
    """Base exception value for the AAYU exception system."""
    def __init__(self, exception_type: str, message: str, error_code: str = "AAYU1000", category: str = "Runtime", stack_trace: List = None):
        self.exception_type = exception_type
        self.message = message
        self.error_code = error_code
        self.category = category
        self.stack_trace = stack_trace if stack_trace is not None else []
    def type_name(self) -> str: return "Exception"
    def truthy(self) -> bool: return True
    def equals(self, other: RuntimeValue) -> bool:
        return isinstance(other, ExceptionValue) and self.exception_type == other.exception_type and self.message == other.message
    def stringify(self) -> str:
        return f"{self.exception_type}: {self.message}"
    def to_python(self) -> Any:
        return {"type": self.exception_type, "message": self.message, "error_code": self.error_code, "category": self.category, "stack_trace": self.stack_trace}
    def clone(self) -> RuntimeValue:
        return ExceptionValue(self.exception_type, self.message, self.error_code, self.category, list(self.stack_trace))

class LanguageException(ExceptionValue):
    """User program exceptions raised via the throw statement."""
    def __init__(self, message: str, stack_trace: List = None):
        super().__init__("LanguageException", message, "AAYU1000", "Language", stack_trace)
    def clone(self) -> RuntimeValue:
        return LanguageException(self.message, list(self.stack_trace))


class RuntimeException(ExceptionValue):
    """VM-originated exceptions raised by the runtime itself."""
    def __init__(self, message: str, stack_trace: List = None):
        super().__init__("RuntimeException", message, "AAYU0000", "Runtime", stack_trace)
    def clone(self) -> RuntimeValue:
        return RuntimeException(self.message, list(self.stack_trace))


class ArithmeticException(RuntimeException):
    """Arithmetic errors (overflow, invalid operations, etc.)."""
    def __init__(self, message: str, stack_trace: List = None):
        super().__init__(message, stack_trace)
        self.exception_type = "ArithmeticException"
        self.error_code = "AAYU0001"
        self.category = "Arithmetic"
    def clone(self) -> RuntimeValue:
        return ArithmeticException(self.message, list(self.stack_trace))


class DivisionByZeroException(ArithmeticException):
    """Division or modulo by zero."""
    def __init__(self, message: str = "Division by zero", stack_trace: List = None):
        super().__init__(message, stack_trace)
        self.exception_type = "DivisionByZero"
        self.error_code = "AAYU0001"
    def clone(self) -> RuntimeValue:
        return DivisionByZeroException(self.message, list(self.stack_trace))


class NullReferenceException(RuntimeException):
    """Attempted operation on a null value."""
    def __init__(self, message: str = "Null reference", stack_trace: List = None):
        super().__init__(message, stack_trace)
        self.exception_type = "NullReference"
        self.error_code = "AAYU0002"
    def clone(self) -> RuntimeValue:
        return NullReferenceException(self.message, list(self.stack_trace))


class IndexOutOfBoundsException(RuntimeException):
    """Index access outside valid range."""
    def __init__(self, message: str = "Index out of bounds", stack_trace: List = None):
        super().__init__(message, stack_trace)
        self.exception_type = "IndexOutOfBounds"
        self.error_code = "AAYU0003"
    def clone(self) -> RuntimeValue:
        return IndexOutOfBoundsException(self.message, list(self.stack_trace))


class ImportException(ExceptionValue):
    """Failed module import."""
    def __init__(self, message: str, stack_trace: List = None):
        super().__init__("ImportException", message, "AAYU0004", "Import", stack_trace)
    def clone(self) -> RuntimeValue:
        return ImportException(self.message, list(self.stack_trace))


class PackageException(ExceptionValue):
    """Package resolution or loading errors."""
    def __init__(self, message: str, stack_trace: List = None):
        super().__init__("PackageException", message, "AAYU0005", "Package", stack_trace)
    def clone(self) -> RuntimeValue:
        return PackageException(self.message, list(self.stack_trace))


class AssertionException(ExceptionValue):
    """Assertion failure."""
    def __init__(self, message: str, stack_trace: List = None):
        super().__init__("AssertionException", message, "AAYU0006", "Assertion", stack_trace)
    def clone(self) -> RuntimeValue:
        return AssertionException(self.message, list(self.stack_trace))


class PanicValue(RuntimeValue):
    """Unrecoverable panic — cannot be caught by try/catch.
    Separate from ExceptionValue to enforce uncatchability at the type level."""
    def __init__(self, message: str, stack_trace: List = None):
        self.message = message
        self.error_code = "AAYU9999"
        self.category = "Panic"
        self.stack_trace = stack_trace if stack_trace is not None else []
    def type_name(self) -> str: return "Panic"
    def truthy(self) -> bool: return True
    def equals(self, other: RuntimeValue) -> bool:
        return isinstance(other, PanicValue) and self.message == other.message
    def stringify(self) -> str:
        return f"PANIC: {self.message}"
    def to_python(self) -> Any:
        return {"message": self.message, "error_code": self.error_code, "category": self.category, "stack_trace": self.stack_trace}
    def clone(self) -> RuntimeValue:
        return PanicValue(self.message, list(self.stack_trace))
