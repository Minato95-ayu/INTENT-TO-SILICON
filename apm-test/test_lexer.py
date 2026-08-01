"""
=============================================================================
FILE: test_lexer.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import sys
sys.path.append('../prototype/aayu_language')
from aayu.compiler.lexer.lexer import Lexer
print([(t.type, t.value) for t in Lexer('return "Status: " + res.status + ", Title: " + res.body.title.').tokenize()])
