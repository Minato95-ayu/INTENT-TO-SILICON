"""
=============================================================================
FILE: diagnostics.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import time
from dataclasses import dataclass
from enum import Enum
from typing import List, Any
from aayu.runtime.values.exception import ExceptionValue, PanicValue

class DiagnosticSeverity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    PANIC = "PANIC"

@dataclass
class RuntimeDiagnostic:
    exception: Any  # ExceptionValue or PanicValue
    stack_trace: List['StackFrame']
    message: str
    severity: DiagnosticSeverity
    timestamp: float
    error_code: str = ""
    category: str = ""
    exit_code: int = 1

class RuntimeDiagnosticFormatter:
    def format(self, diagnostic: RuntimeDiagnostic) -> str:
        code_str = f" [{diagnostic.error_code}]" if diagnostic.error_code else ""
        lines = [f"{diagnostic.severity.value}{code_str}"]
        lines.append("")
        lines.append(diagnostic.message)
        
        if diagnostic.stack_trace:
            lines.append("")
            lines.append("Location")
            lines.append("")
            
            # The top frame is where the exception occurred
            top_frame = diagnostic.stack_trace[0]
            filename = "unknown"
            if hasattr(diagnostic.exception, 'debug_info') and diagnostic.exception.debug_info:
                if top_frame.span.file_id in diagnostic.exception.debug_info.source_files:
                    filename = diagnostic.exception.debug_info.source_files[top_frame.span.file_id].path
            
            lines.append(f"{filename}:{top_frame.span.start_line}:{top_frame.span.start_column}")
            lines.append("")
            lines.append("Call Stack")
            lines.append("")
            
            for fi in diagnostic.stack_trace:
                frame_filename = "unknown"
                if hasattr(diagnostic.exception, 'debug_info') and diagnostic.exception.debug_info:
                    if fi.span.file_id in diagnostic.exception.debug_info.source_files:
                        frame_filename = diagnostic.exception.debug_info.source_files[fi.span.file_id].path
                
                lines.append(f"at {fi.module}.{fi.function}()")
                # Avoid repeating location if it's the top frame? Actually the user format had it at every frame.
                # Actually in the user example it was:
                # at math.divide()
                # at calculator.compute()
                # I'll include the location for each frame like user did or just the function?
                # User's sample didn't have location on every call stack frame, only on top level and a few others?
                # I'll just include it.
                # lines.append(f"{frame_filename}:{fi.span.start_line}:{fi.span.start_column}")
                # lines.append("")
        return "\n".join(lines).strip()

class AAYUUnhandledException(Exception):
    def __init__(self, diagnostic: RuntimeDiagnostic):
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic

