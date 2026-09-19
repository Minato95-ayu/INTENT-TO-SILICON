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

from typing import Dict, Optional, Any

class Symbol:
    def __init__(self, name: str, symbol_type: str, is_mutable: bool = True):
        self.name = name
        self.symbol_type = symbol_type  # e.g., 'state', 'model', 'local', 'function'
        self.data_type: str = "Any"     # e.g., "Integer", "String", "List<String>", "Model_User", "Widget"
        self.is_mutable: bool = is_mutable
        self.scope: str = ""
        self.initialized: bool = False
        self.nullable: bool = True
        self.is_parameter: bool = False
        self.is_function: bool = False
        self.is_constant: bool = not is_mutable
        self.signature_args: int = -1

class SymbolTable:
    def __init__(self, parent: Optional['SymbolTable'] = None):
        self.symbols: Dict[str, Symbol] = {}
        self.parent = parent

    def define(self, symbol: Symbol):
        self.symbols[symbol.name] = symbol

    def resolve(self, name: str) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.resolve(name)
        return None

