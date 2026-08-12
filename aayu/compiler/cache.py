import os
import json
import shutil
import time
from typing import Dict, Any, Optional

from aayu.compiler.graph import ModuleGraph, ModuleNode

class IncrementalCache:
    """
    Manages the disk-based incremental cache for the compiler.
    Enforces deterministic build tracking, cryptographic hashing, and automated recovery.
    """
    COMPILER_VERSION = "1.0.0"
    EDITION = "2026"
    IR_VERSION = "1"
    BYTECODE_VERSION = "1"
    ABI_VERSION = "1"

    def __init__(self, root_dir: str):
        self.cache_dir = os.path.join(root_dir, ".aayu_cache")
        self.metadata_path = os.path.join(self.cache_dir, "metadata.json")
        self.manifest_path = os.path.join(root_dir, "build_manifest.json")
        self.metadata = {}

    def init_cache(self):
        try:
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)
                self._create_empty_metadata()
            else:
                if not os.path.exists(self.metadata_path):
                    self._create_empty_metadata()
                else:
                    with open(self.metadata_path, "r") as f:
                        self.metadata = json.load(f)
                    
                    # Compiler Version Lock check
                    if self.metadata.get("compiler_version") != self.COMPILER_VERSION:
                        self.recover_cache("Compiler version changed. Invalidating cache.")
        except Exception as e:
            # Recovery Mode (Mandatory): Never crash on cache errors
            self.recover_cache(f"Cache Corrupted ({str(e)}).")

    def _create_empty_metadata(self):
        self.metadata = {
            "compiler_version": self.COMPILER_VERSION,
            "modules": {}
        }
        self.save_metadata()

    def recover_cache(self, reason: str = "Unknown"):
        print(f"[CACHE] {reason} Cleaning Cache -> Rebuilding...")
        if os.path.exists(self.cache_dir):
            try:
                shutil.rmtree(self.cache_dir)
            except Exception:
                pass
        os.makedirs(self.cache_dir, exist_ok=True)
        self._create_empty_metadata()

    def save_metadata(self):
        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def get_ast_path(self, node_id: str) -> str:
        import hashlib
        safe_name = hashlib.md5(node_id.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{safe_name}.ast")

    def save_ast(self, node_id: str, ast_obj: Any):
        import pickle
        with open(self.get_ast_path(node_id), "wb") as f:
            pickle.dump(ast_obj, f)

    def load_ast(self, node_id: str) -> Optional[Any]:
        import pickle
        path = self.get_ast_path(node_id)
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return pickle.load(f)
            except Exception:
                pass
        return None

    def is_module_up_to_date(self, node: ModuleNode) -> bool:
        """
        Determines if a module can be safely skipped based on SHA-256 hashes.
        Validates both source_hash and dep_hash.
        """
        mod_cache = self.metadata.get("modules", {}).get(node.id)
        if not mod_cache:
            return False
            
        if mod_cache.get("source_hash") != node.source_hash:
            return False
            
        if mod_cache.get("dep_hash") != node.dep_hash:
            return False
            
        return True
        
    def update_module_cache(self, node: ModuleNode):
        if "modules" not in self.metadata:
            self.metadata["modules"] = {}
            
        self.metadata["modules"][node.id] = {
            "source_hash": node.source_hash,
            "ast_hash": node.ast_hash,
            "hir_hash": node.hir_hash,
            "mir_hash": node.mir_hash,
            "dep_hash": node.dep_hash,
            "compile_state": node.compile_state
        }
        self.save_metadata()

    def generate_build_manifest(self, graph: ModuleGraph, compile_time_ms: float, warnings: int, errors: int):
        """
        Generates the mandatory build_manifest.json tracking determinism and outputs.
        """
        manifest = {
            "build_timestamp": time.time(),
            "compile_time_ms": compile_time_ms,
            "compiler": {
                "version": self.COMPILER_VERSION,
                "edition": self.EDITION,
                "ir_version": self.IR_VERSION,
                "bytecode_version": self.BYTECODE_VERSION,
                "abi_version": self.ABI_VERSION
            },
            "diagnostics": {
                "warnings": warnings,
                "errors": errors
            },
            "modules": {}
        }
        
        for node_id, node in graph.nodes.items():
            manifest["modules"][node_id] = {
                "source_hash": node.source_hash,
                "dep_hash": node.dep_hash,
                "ast_hash": node.ast_hash,
                "hir_hash": node.hir_hash,
                "mir_hash": node.mir_hash,
                "compile_state": node.compile_state
            }
            
        with open(self.manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
            
class BuildPlanner:
    """
    Orchestrates the build process based on Graph States and Incremental Cache.
    """
    def __init__(self, graph: ModuleGraph, cache: IncrementalCache):
        self.graph = graph
        self.cache = cache
        
    def plan(self):
        self.cache.init_cache()
        order = self.graph.kahn_topological_sort()
        
        # 1. Compute dep_hashes exactly according to topological order
        # This is safe because a node's dependencies are already processed.
        for node in order:
            node.compute_dep_hash()
            
        # 2. Determine actions
        actions = {}
        for node in order:
            if self.cache.is_module_up_to_date(node):
                actions[node.id] = "Skip"
            else:
                actions[node.id] = "Compile"
                
        return order, actions
