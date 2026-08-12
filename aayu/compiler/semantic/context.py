from typing import Dict, Any, Optional, List
from aayu.compiler.semantic.symbols import ProjectScope
from aayu.compiler.semantic.diagnostics import DiagnosticEngine, Diagnostic

import hashlib

class IDCollisionError(Exception):
    def __init__(self, id_val: int, existing_name: str, new_name: str, phase: str):
        import platform
        super().__init__(
            f"\nIDCollisionError\n"
            f"Phase: {phase}\n"
            f"ID: {id_val}\n"
            f"Existing canonical identity: {existing_name}\n"
            f"Conflicting canonical identity: {new_name}\n"
            f"Compiler Version: prototype (python {platform.python_version()})"
        )

class TypeID(int):
    pass

class SymbolID(int):
    pass

class SymbolRegistry:
    def __init__(self):
        # Maps node_id to resolved QualifiedSymbol (or Symbol ID)
        self.resolved_symbols: Dict[int, Any] = {}
        # Track generated symbol IDs to detect collisions
        self._symbol_ids_by_name: Dict[str, SymbolID] = {}
        self._name_by_symbol_id: Dict[SymbolID, str] = {}
        
    def _generate_symbol_id(self, qualified_name: str) -> SymbolID:
        import hashlib
        hash_bytes = hashlib.sha256(qualified_name.encode('utf-8')).digest()
        int_id = int.from_bytes(hash_bytes[:8], byteorder='big')
        sid = SymbolID(int_id)
        
        if sid in self._name_by_symbol_id and self._name_by_symbol_id[sid] != qualified_name:
            raise IDCollisionError(sid, self._name_by_symbol_id[sid], qualified_name, "SemanticContext / SymbolRegistry")
            
        self._symbol_ids_by_name[qualified_name] = sid
        self._name_by_symbol_id[sid] = qualified_name
        return sid
        
    def get_symbol_id(self, module_id: str, symbol_name: str) -> SymbolID:
        return self._generate_symbol_id(f"{module_id}::{symbol_name}")

class TypeRegistry:
    def __init__(self):
        # Maps node_id to inferred Type
        self.resolved_types: Dict[int, Any] = {}
        # Maps Qualified ID (e.g. "core::Point") to the actual Type object
        self.registered_types: Dict[str, Any] = {}
        # Maps TypeID (deterministic int) to the actual Type object
        self.type_by_id: Dict[TypeID, Any] = {}
        # Maps Qualified ID to TypeID
        self.id_by_qualified: Dict[str, TypeID] = {}
        
        # Track names by type id for collision detection
        self._name_by_type_id: Dict[TypeID, str] = {}
        self._register_builtins()
        
    def _register_builtins(self):
        from aayu.compiler.semantic.types import (
            T_INT, T_FLOAT, T_STRING, T_BOOL, T_CHAR, T_BYTE,
            T_VOID, T_NEVER, T_ANY, T_NULL
        )
        # Register primitives with standard qualified names like "core::Int"
        primitives = [
            T_INT, T_FLOAT, T_STRING, T_BOOL, T_CHAR, T_BYTE,
            T_VOID, T_NEVER, T_ANY, T_NULL
        ]
        for p in primitives:
            self.register_type(f"core::{p.name}", p)
        
    def _generate_type_id(self, qualified_id: str) -> TypeID:
        # Deterministic hashing (e.g. FNV-1a or SHA-256 truncated)
        # Using SHA-256 first 8 bytes for a 64-bit integer ID
        hash_bytes = hashlib.sha256(qualified_id.encode('utf-8')).digest()
        int_id = int.from_bytes(hash_bytes[:8], byteorder='big')
        tid = TypeID(int_id)
        
        if tid in self._name_by_type_id and self._name_by_type_id[tid] != qualified_id:
            raise IDCollisionError(tid, self._name_by_type_id[tid], qualified_id, "SemanticContext / TypeRegistry")
            
        self._name_by_type_id[tid] = qualified_id
        return tid
        
    def register_type(self, qualified_id: str, type_obj: Any) -> TypeID:
        self.registered_types[qualified_id] = type_obj
        tid = self._generate_type_id(qualified_id)
        self.type_by_id[tid] = type_obj
        self.id_by_qualified[qualified_id] = tid
        return tid
        
    def get_type(self, qualified_id: str) -> Optional[Any]:
        return self.registered_types.get(qualified_id)
        
    def get_type_by_id(self, type_id: TypeID) -> Optional[Any]:
        return self.type_by_id.get(type_id)
        
    def get_id(self, qualified_id: str) -> Optional[TypeID]:
        return self.id_by_qualified.get(qualified_id)

class ModuleRegistry:
    def __init__(self):
        # Maps module ID to metadata or exports
        self.modules: Dict[str, Any] = {}

class DiagnosticRegistry:
    def __init__(self, engine: DiagnosticEngine):
        self.engine = engine
        self.diagnostics: List[Diagnostic] = []
        
    def add(self, diag: Diagnostic):
        self.diagnostics.append(diag)
        try:
            self.engine.report(diag) # New engine
        except TypeError:
            # Legacy engine
            from aayu.compiler.errors import DiagnosticSeverity as LegacySeverity
            sev = LegacySeverity.ERROR
            if diag.severity.name == "WARNING": sev = LegacySeverity.WARNING
            elif diag.severity.name == "INFO": sev = LegacySeverity.INFO
            self.engine.report(sev, diag.message, getattr(diag, "span", None), getattr(diag, "hint", None))

class SourceMap:
    def __init__(self):
        # node_id -> (file_path, line, column, offset, length)
        self.locations: Dict[int, tuple] = {}
        
    def register(self, node_id: int, file_path: str, line: int, column: int, offset: int = 0, length: int = 0):
        self.locations[node_id] = (file_path, line, column, offset, length)
        
    def get_location(self, node_id: int) -> Optional[tuple]:
        return self.locations.get(node_id)

class SemanticContext:
    """
    AAYU Semantic Context (Constitution v1.0)
    The single source of truth for all semantic passes. AST nodes are immutable,
    and all metadata derived by passes is stored in these registries.
    """
    def __init__(self, diag_engine: DiagnosticEngine, project_scope: ProjectScope = None):
        self.project_scope = project_scope
        self.symbol_registry = SymbolRegistry()
        self.type_registry = TypeRegistry()
        self.module_registry = ModuleRegistry()
        self.diagnostic_registry = DiagnosticRegistry(diag_engine)
        self.source_map = SourceMap()
        
        # Future proof registries (Interfaces frozen, implemented lazily when Language Spec requires)
        # self.trait_registry = None
        # self.generic_registry = None
        # self.ownership_registry = None
        # self.lifetime_registry = None
        
        # Legacy node scopes compatibility until fully migrated
        self.node_scopes: Dict[int, Any] = {}
