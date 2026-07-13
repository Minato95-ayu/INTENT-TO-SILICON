import os
from .manifest import Manifest
from .lockfile import LockFile
from .cache import CacheManager
from .resolver import Resolver
from .downloader import Downloader
from .installer import Installer
from .publisher import Publisher
from .auth import Auth
from .official_registry import OfficialRegistry
from .github_registry import GithubRegistry
from .tree import TreePrinter

class PackageManager:
    """Orchestrates all package management commands."""
    
    def __init__(self, root_dir: str = ".", mock_home: str = None):
        self.root_dir = root_dir
        self.modules_dir = os.path.join(root_dir, ".aayu_modules")
        
        # Core components
        self.cache = CacheManager(home_dir=mock_home)
        self.auth = Auth(home_dir=mock_home)
        self.registry = OfficialRegistry(self.cache.cache_dir)
        
        self.resolver = Resolver(self.registry)
        self.downloader = Downloader(self.registry, self.cache)
        self.installer = Installer(self.modules_dir)
        self.publisher = Publisher(self.registry)
        
    def init(self):
        manifest_path = os.path.join(self.root_dir, "aayu.json")
        Manifest.create_default(manifest_path, os.path.basename(os.path.abspath(self.root_dir)))
        print("Initialized aayu.json")
        
    def install(self, package_name: str = None, source: str = None):
        manifest_path = os.path.join(self.root_dir, "aayu.json")
        manifest = Manifest.load(manifest_path)
        
        if package_name:
            # Install specific package
            if source and source.startswith("github:"):
                # Stub for github installs
                print(f"Installing {package_name} from {source}...")
                manifest.data["dependencies"][package_name] = source
            else:
                # Add to manifest
                req = source if source else "^1.0.0"
                manifest.data["dependencies"][package_name] = req
            manifest.save()
            print(f"Added {package_name} to aayu.json dependencies.")
            
        # Resolve all dependencies
        resolved_graph = self.resolver.resolve(manifest.dependencies)
        
        # Download, cache, and install
        lock = LockFile.load(os.path.join(self.root_dir, "aayu.lock"))
        
        for name, meta in resolved_graph.items():
            version = meta["version"]
            checksum = meta["checksum"]
            
            zip_path = self.downloader.fetch(name, version)
            self.installer.install(name, zip_path, checksum)
            
            lock.update_package(name, version, checksum, meta["dependencies"])
            print(f"Installed {name}@{version}")
            
        lock.save()
        print("Installation complete.")
        
    def remove(self, package_name: str):
        manifest_path = os.path.join(self.root_dir, "aayu.json")
        manifest = Manifest.load(manifest_path)
        
        if package_name in manifest.dependencies:
            del manifest.data["dependencies"][package_name]
            manifest.save()
            print(f"Removed {package_name} from aayu.json.")
            
        if self.installer.remove(package_name):
            print(f"Removed {package_name} from .aayu_modules.")
        else:
            print(f"Package {package_name} not found in .aayu_modules.")
            
    def update(self):
        print("Updating packages (ignoring lockfile)...")
        # To update, we just delete the lockfile and reinstall
        lock_path = os.path.join(self.root_dir, "aayu.lock")
        if os.path.exists(lock_path):
            os.remove(lock_path)
        self.install()
        
    def list_packages(self):
        lock = LockFile.load(os.path.join(self.root_dir, "aayu.lock"))
        print("Installed Packages:")
        for name, meta in lock.data.get("packages", {}).items():
            print(f"- {name}@{meta['version']}")
            
    def search(self, query: str):
        results = self.registry.search(query)
        print(f"Search results for '{query}':")
        for res in results:
            print(f"- {res['name']} ({res['description']}) by {res['owner']}")
            
    def tree(self):
        manifest_path = os.path.join(self.root_dir, "aayu.json")
        manifest = Manifest.load(manifest_path)
        
        lock = LockFile.load(os.path.join(self.root_dir, "aayu.lock"))
        graph = {}
        for name, meta in lock.data.get("packages", {}).items():
            graph[name] = list(meta.get("dependencies", {}).keys())
            
        # Add root
        graph[manifest.name] = list(manifest.dependencies.keys())
        
        TreePrinter.print_tree(manifest.name, graph)
        
    def publish(self):
        if not self.auth.is_logged_in():
            print("You must be logged in to publish. Run 'aayu login'.")
            return
            
        name, version = self.publisher.publish(self.root_dir)
        print(f"Successfully published {name}@{version} to registry.")
        
    def login(self, token: str):
        self.auth.login(token)
        print("Logged in successfully.")
        
    def logout(self):
        self.auth.logout()
        print("Logged out successfully.")
