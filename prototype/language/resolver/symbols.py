from enum import Enum, auto
from typing import Dict, Optional, Any

class SymbolKind(Enum):
    MODULE = auto()
    FUNCTION = auto()
    VARIABLE = auto()
    PARAMETER = auto()
    BUILTIN = auto()
    IMPORT = auto()
    INTERFACE = auto()

class TypeSource(Enum):
    EXPLICIT = "explicit"
    INFERRED = "inferred"
    GENERIC = "generic"
    BUILTIN = "builtin"

class Symbol:
    _id_counter = 0

    def __init__(self, name: str, kind: SymbolKind, scope: 'SymbolTable', owner: Any = None, is_exported: bool = False, visibility: str = "private"):
        Symbol._id_counter += 1
        self.id = Symbol._id_counter
        self.name = name
        self.kind = kind
        self.scope = scope
        self.owner = owner
        self.is_exported = is_exported
        self.visibility = visibility
        
        # Phase 5.2 - Semantic Type Layer
        self.declared_type: Any = None
        self.resolved_type: Any = None
        self.type_source: str = TypeSource.EXPLICIT.value
        
    def __repr__(self):
        return f"<{self.kind.name} {self.name} (id={self.id})>"

class ModuleSymbol(Symbol):
    def __init__(self, name: str, scope: 'SymbolTable', module_table: 'SymbolTable'):
        super().__init__(name, SymbolKind.MODULE, scope)
        self.module_table = module_table

class FunctionSymbol(Symbol):
    def __init__(self, name: str, scope: 'SymbolTable', is_exported: bool = False, visibility: str = "private"):
        super().__init__(name, SymbolKind.FUNCTION, scope, is_exported=is_exported, visibility=visibility)

class VariableSymbol(Symbol):
    def __init__(self, name: str, scope: 'SymbolTable', is_exported: bool = False, visibility: str = "private"):
        super().__init__(name, SymbolKind.VARIABLE, scope, is_exported=is_exported, visibility=visibility)

class ParameterSymbol(Symbol):
    def __init__(self, name: str, scope: 'SymbolTable'):
        super().__init__(name, SymbolKind.PARAMETER, scope)

class BuiltinSymbol(Symbol):
    def __init__(self, name: str, scope: 'SymbolTable'):
        super().__init__(name, SymbolKind.BUILTIN, scope)

class InterfaceSymbol(Symbol):
    def __init__(self, name: str, scope: 'SymbolTable', is_exported: bool = False, visibility: str = "private"):
        super().__init__(name, SymbolKind.INTERFACE, scope, is_exported=is_exported, visibility=visibility)

class ScopeType(Enum):
    BUILTIN = auto()
    GLOBAL = auto()
    MODULE = auto()
    FUNCTION = auto()
    LOCAL = auto()

class SymbolTable:
    def __init__(self, name: str, scope_type: ScopeType, parent: Optional['SymbolTable'] = None):
        self.name = name
        self.scope_type = scope_type
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}

    def define(self, symbol: Symbol):
        if symbol.name in self.symbols:
            raise Exception(f"Duplicate symbol '{symbol.name}' in scope '{self.name}'")
        self.symbols[symbol.name] = symbol

    def lookup(self, name: str, current_only: bool = False) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if current_only or self.parent is None:
            return None
        return self.parent.lookup(name)
