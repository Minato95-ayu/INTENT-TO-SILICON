from enum import Enum
from dataclasses import dataclass
from typing import Optional
from location import SourceSpan

class ExecutionMode(Enum):
    RUN = "RUN"
    PAUSED = "PAUSED"
    STEP_INTO = "STEP_INTO"
    STEP_OVER = "STEP_OVER"
    STEP_OUT = "STEP_OUT"

@dataclass
class Breakpoint:
    id: int
    module: str
    enabled: bool = True
    instruction_pointer: Optional[int] = None
    span: Optional[SourceSpan] = None
