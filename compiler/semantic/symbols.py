from typing import Dict, Optional, Any

class Symbol:
    def __init__(self, name: str, symbol_type: str, is_mutable: bool = True):
        self.name = name
        self.symbol_type = symbol_type
        self.is_mutable = is_mutable

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
