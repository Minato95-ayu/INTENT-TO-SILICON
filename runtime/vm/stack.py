"""
=============================================================================
FILE: stack.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

class Stack:
    def __init__(self):
        self._stack = []

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        if not self._stack:
            raise IndexError("pop from empty stack")
        return self._stack.pop()
        
    def peek(self):
        if not self._stack:
            raise IndexError("peek from empty stack")
        return self._stack[-1]
        
    def is_empty(self):
        return len(self._stack) == 0

    def __len__(self):
        return len(self._stack)
