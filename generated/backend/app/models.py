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

from pydantic import BaseModel
from typing import Optional, List

class Patient(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class Doctor(BaseModel):
    name: Optional[str] = None


