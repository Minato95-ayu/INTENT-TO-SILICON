# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

"""
=============================================================================
FILE: models.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional
from compiler.frontend.location import SourceSpan

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
