import os
from pathlib import Path
from typing import Optional, List, Dict

class Loader:
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.module_paths: Dict[str, Path] = {}
        self.source_roots: List[Path] = [
            workspace_root / "src",
            workspace_root / "packages"
        ]
        
    def find_module(self, module_name: str, current_file: Optional[Path] = None) -> Optional[Path]:
        if module_name in self.module_paths:
            return self.module_paths[module_name]
            
        file_name = f"{module_name}.aayu"
        
        # Check source roots
        for root in self.source_roots:
            if not root.exists():
                continue
                
            # If it's a package, check inside package's src directory
            pkg_src = root / module_name / "src" / file_name
            if pkg_src.exists():
                return pkg_src
                
            # Otherwise check directly in the root (like src/math.aayu)
            direct = root / file_name
            if direct.exists():
                return direct

        """
        Locates the physical file for a given module name.
        Example: `math` -> `math.aayu`
        """
        # Module name to relative path
        rel_path = module_name.replace('.', os.sep) + ".aayu"
        
        # 1. Check relative to current file if available
        if current_file:
            candidate = current_file.parent / rel_path
            if candidate.exists() and candidate.is_file():
                return candidate
                
        # 2. Check workspace root
        candidate = self.workspace_root / rel_path
        if candidate.exists() and candidate.is_file():
            return candidate
            
        # 3. Check src/ in workspace
        candidate = self.workspace_root / "src" / rel_path
        if candidate.exists() and candidate.is_file():
            return candidate
            
        return None
        
    def load_source(self, file_path: Path) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
