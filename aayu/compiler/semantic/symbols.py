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

class ModuleSymbol(Symbol):
    def __init__(self, name: str, module_id: str):
        super().__init__(name, "module", is_mutable=False)
        self.module_id = module_id
        self.exports: SymbolTable = SymbolTable()

class ProjectScope:
    def __init__(self):
        self._modules: Dict[str, ModuleSymbol] = {}
        self._is_frozen = False
        
    def add_module(self, module: ModuleSymbol):
        if self._is_frozen:
            raise RuntimeError("Cannot add module to a frozen ProjectScope")
        self._modules[module.module_id] = module
        
    def get_module(self, module_id: str) -> Optional[ModuleSymbol]:
        return self._modules.get(module_id)
        
    def freeze(self):
        self._is_frozen = True
        
    @property
    def modules(self) -> Dict[str, ModuleSymbol]:
        return dict(self._modules)
