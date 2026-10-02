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
FILE: collection.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from .reference import ReferenceValue
from .base import RuntimeValue
from abc import abstractmethod
from typing import Any

class CollectionValue(ReferenceValue):
    
    @abstractmethod
    def length(self) -> RuntimeValue:
        pass
        
    @abstractmethod
    def get(self, key: RuntimeValue) -> RuntimeValue:
        pass
        
    @abstractmethod
    def set(self, key: RuntimeValue, value: RuntimeValue):
        pass
        
    @abstractmethod
    def append(self, value: RuntimeValue):
        pass
        
    @abstractmethod
    def remove(self, key: RuntimeValue):
        pass
        
    @abstractmethod
    def contains(self, value: RuntimeValue) -> RuntimeValue:
        pass
        
    @abstractmethod
    def iterate(self):
        pass
