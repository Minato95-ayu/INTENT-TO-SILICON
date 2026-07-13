from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional

class ResultStatus(Enum):
    OK = 0
    ERROR = 1
    TIMEOUT = 2
    PANIC = 3

@dataclass
class RuntimeResult:
    """Wraps the result of a Kernel/Plugin operation."""
    status: ResultStatus
    value: Any = None
    error_message: Optional[str] = None
    
    @classmethod
    def ok(cls, value=None):
        return cls(ResultStatus.OK, value=value)
        
    @classmethod
    def error(cls, message: str):
        return cls(ResultStatus.ERROR, error_message=message)
