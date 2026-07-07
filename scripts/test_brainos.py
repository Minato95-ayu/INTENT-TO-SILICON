"""
=============================================================================
FILE: test_brainos.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import sys
import os

sys.path.append(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype')

from brainos.orchestrator import BrainOSOrchestrator

orchestrator = BrainOSOrchestrator(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine\knowledge')
# A simple sentence that uses defined keywords
# Entities in KB: Student, Teacher, Course
# Fields in KB: age, name
intent = "Create a Student system with age and name."
files = orchestrator.process_intent(intent)

for filename, content in files.items():
    print(f"--- {filename} ---")
    print(content)
