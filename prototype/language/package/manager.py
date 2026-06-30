from manifest.model import PackageManifest
from compiler_context import Diagnostics
from .resolver import DependencyResolver
from .installer import PackageInstaller
from .registry import RegistryClient

class PackageManager:
    def __init__(self, diagnostics: Diagnostics, registry: RegistryClient, packages_dir: str):
        self.diagnostics = diagnostics
        self.registry = registry
        self.packages_dir = packages_dir
        
    def ensure_dependencies(self, manifest: PackageManifest) -> bool:
        resolver = DependencyResolver(self.diagnostics, self.registry)
        graph = resolver.resolve(manifest)
        
        if self.diagnostics.has_errors():
            return False
            
        installer = PackageInstaller(self.diagnostics, self.registry, self.packages_dir)
        success = installer.install(graph, manifest.package.name)
        
        return success and not self.diagnostics.has_errors()
