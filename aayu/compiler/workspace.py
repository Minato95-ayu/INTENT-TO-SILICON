import tomllib
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass(frozen=True)
class PackageManifest:
    name: str
    version: str
    edition: str = "2026"
    entry: str = "main.aayu"

@dataclass(frozen=True)
class CompilerOptions:
    target: str = "native"
    optimization: str = "release"
    warnings_as_errors: bool = True

@dataclass(frozen=True)
class AayuProjectConfig:
    package: PackageManifest
    compiler: CompilerOptions = field(default_factory=CompilerOptions)
    dependencies: Dict[str, str] = field(default_factory=dict)
    workspace_members: List[str] = field(default_factory=list)
    dir_path: str = "" # Absolute path to the directory containing Aayu.toml

class WorkspaceLoader:
    """
    Loads a primary Aayu.toml and discovers workspace members (monorepo).
    """
    def __init__(self, root_dir: str):
        self.root_dir = os.path.abspath(root_dir)
        self.toml_path = os.path.join(self.root_dir, "Aayu.toml")
        self.config: Optional[AayuProjectConfig] = None
        self.members: Dict[str, AayuProjectConfig] = {} # pkg_name -> config
        
    def _parse_toml(self, toml_path: str, dir_path: str) -> AayuProjectConfig:
        if not os.path.exists(toml_path):
            raise FileNotFoundError(f"Missing Aayu.toml at {toml_path}")
            
        with open(toml_path, "rb") as f:
            try:
                data = tomllib.load(f)
            except tomllib.TOMLDecodeError as e:
                raise ValueError(f"Invalid Aayu.toml at {toml_path}: {e}")
                
        pkg_data = data.get("package", {})
        if "name" not in pkg_data or "version" not in pkg_data:
            raise ValueError(f"Aayu.toml at {toml_path} must contain [package] with 'name' and 'version'")
            
        package = PackageManifest(
            name=pkg_data["name"],
            version=pkg_data["version"],
            edition=pkg_data.get("edition", "2026"),
            entry=pkg_data.get("entry", "main.aayu")
        )
        
        comp_data = data.get("compiler", {})
        compiler = CompilerOptions(
            target=comp_data.get("target", "native"),
            optimization=comp_data.get("optimization", "release"),
            warnings_as_errors=comp_data.get("warnings_as_errors", True)
        )
        
        deps = data.get("dependencies", {})
        ws_data = data.get("workspace", {})
        ws_members = ws_data.get("members", [])
        
        return AayuProjectConfig(
            package=package,
            compiler=compiler,
            dependencies=deps,
            workspace_members=ws_members,
            dir_path=dir_path
        )

    def load(self) -> AayuProjectConfig:
        self.config = self._parse_toml(self.toml_path, self.root_dir)
        self.members[self.config.package.name] = self.config
        
        # Load workspace members (Monorepo)
        for member_dir_name in self.config.workspace_members:
            member_path = os.path.join(self.root_dir, member_dir_name)
            member_toml = os.path.join(member_path, "Aayu.toml")
            if os.path.exists(member_toml):
                member_config = self._parse_toml(member_toml, member_path)
                self.members[member_config.package.name] = member_config
                
        return self.config

class PackageResolver:
    """
    Resolves logical dependencies (e.g. auth = "1.0") to physical entry files.
    Abstracts away file paths from the rest of the compiler.
    """
    def __init__(self, workspace: WorkspaceLoader):
        self.workspace = workspace
        
    def resolve(self, package_name: str) -> Optional[str]:
        """
        Returns the absolute path to the main.aayu entry file for the given package.
        """
        if package_name in self.workspace.members:
            config = self.workspace.members[package_name]
            return os.path.join(config.dir_path, config.package.entry)
        
        # In the future, this is where we check global package caches (~/.aayu/packages)
        return None
