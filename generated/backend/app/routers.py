"""
=============================================================================
FILE: routers.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from fastapi import APIRouter
from typing import List
from app.models import Patient, Doctor

router = APIRouter()

@router.get('/patients', response_model=List[Patient])
def get_patients():
    return []

@router.get('/doctors', response_model=List[Doctor])
def get_doctors():
    return []


