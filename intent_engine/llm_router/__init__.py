"""
=============================================================================
FILE: __init__.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from .base import LLMRouter
from .connectors import OpenAIConnector, GeminiConnector

__all__ = [
    'LLMRouter',
    'OpenAIConnector',
    'GeminiConnector'
]
