import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aayu.compiler.workspace import WorkspaceLoader, PackageResolver

def test_package_resolver():
    test_dir = os.path.join(os.path.dirname(__file__), "mock_monorepo")
    os.makedirs(test_dir, exist_ok=True)
    
    # Root Aayu.toml
    root_toml = """
    [package]
    name = "hospital"
    version = "1.0.0"
    
    [dependencies]
    auth = "1.0"
    db = "2.1"
    
    [workspace]
    members = ["auth", "db"]
    """
    
    # Auth package Aayu.toml
    auth_dir = os.path.join(test_dir, "auth")
    os.makedirs(auth_dir, exist_ok=True)
    auth_toml = """
    [package]
    name = "auth"
    version = "1.0.0"
    entry = "auth_main.aayu"
    """
    
    # DB package Aayu.toml
    db_dir = os.path.join(test_dir, "db")
    os.makedirs(db_dir, exist_ok=True)
    db_toml = """
    [package]
    name = "db"
    version = "2.1.0"
    entry = "db_main.aayu"
    """
    
    with open(os.path.join(test_dir, "Aayu.toml"), "w") as f: f.write(root_toml)
    with open(os.path.join(auth_dir, "Aayu.toml"), "w") as f: f.write(auth_toml)
    with open(os.path.join(db_dir, "Aayu.toml"), "w") as f: f.write(db_toml)
    
    # Test Loading
    loader = WorkspaceLoader(test_dir)
    loader.load()
    
    assert "hospital" in loader.members
    assert "auth" in loader.members
    assert "db" in loader.members
    
    # Test Resolving
    resolver = PackageResolver(loader)
    auth_entry = resolver.resolve("auth")
    db_entry = resolver.resolve("db")
    
    assert auth_entry == os.path.abspath(os.path.join(auth_dir, "auth_main.aayu"))
    assert db_entry == os.path.abspath(os.path.join(db_dir, "db_main.aayu"))
    assert resolver.resolve("unknown") is None
    
    print("[OK] PackageResolver successfully mapped monorepo dependencies!")

if __name__ == "__main__":
    test_package_resolver()
