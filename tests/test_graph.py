import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aayu.compiler.workspace import WorkspaceLoader
from aayu.compiler.graph import ModuleGraph

def test_topological_sort():
    test_dir = os.path.join(os.path.dirname(__file__), "mock_graph_clean")
    os.makedirs(test_dir, exist_ok=True)
    
    # Root
    root_toml = """
    [package]
    name = "main"
    version = "1.0.0"
    [workspace]
    members = ["auth", "db", "models"]
    """
    with open(os.path.join(test_dir, "Aayu.toml"), "w") as f: f.write(root_toml)
    with open(os.path.join(test_dir, "main.aayu"), "w") as f: f.write("import auth\nimport db\n")
    
    # Auth
    auth_dir = os.path.join(test_dir, "auth")
    os.makedirs(auth_dir, exist_ok=True)
    with open(os.path.join(auth_dir, "Aayu.toml"), "w") as f: f.write("[package]\nname = 'auth'\nversion = '1.0'\n")
    with open(os.path.join(auth_dir, "main.aayu"), "w") as f: f.write("import db\nimport models\n")
    
    # DB
    db_dir = os.path.join(test_dir, "db")
    os.makedirs(db_dir, exist_ok=True)
    with open(os.path.join(db_dir, "Aayu.toml"), "w") as f: f.write("[package]\nname = 'db'\nversion = '1.0'\n")
    with open(os.path.join(db_dir, "main.aayu"), "w") as f: f.write("import models\n")
    
    # Models
    models_dir = os.path.join(test_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    with open(os.path.join(models_dir, "Aayu.toml"), "w") as f: f.write("[package]\nname = 'models'\nversion = '1.0'\n")
    with open(os.path.join(models_dir, "main.aayu"), "w") as f: f.write("// Leaf node\n")
    
    loader = WorkspaceLoader(test_dir)
    loader.load()
    
    graph = ModuleGraph(loader)
    graph.build_graph()
    
    order = graph.kahn_topological_sort()
    names = [node.id for node in order]
    
    # Bottom up order
    # models -> db -> auth -> main
    assert names == ["models", "db", "auth", "main"], f"Got {names}"
    print("[OK] Kahn's Topological Sort passed!")

def test_circular_dependency():
    test_dir = os.path.join(os.path.dirname(__file__), "mock_graph_cycle")
    os.makedirs(test_dir, exist_ok=True)
    
    root_toml = """
    [package]
    name = "main"
    version = "1.0.0"
    [workspace]
    members = ["auth", "db", "models"]
    """
    with open(os.path.join(test_dir, "Aayu.toml"), "w") as f: f.write(root_toml)
    with open(os.path.join(test_dir, "main.aayu"), "w") as f: f.write("import auth\n")
    
    # Auth
    auth_dir = os.path.join(test_dir, "auth")
    os.makedirs(auth_dir, exist_ok=True)
    with open(os.path.join(auth_dir, "Aayu.toml"), "w") as f: f.write("[package]\nname = 'auth'\nversion = '1.0'\n")
    with open(os.path.join(auth_dir, "main.aayu"), "w") as f: f.write("import db\n")
    
    # DB
    db_dir = os.path.join(test_dir, "db")
    os.makedirs(db_dir, exist_ok=True)
    with open(os.path.join(db_dir, "Aayu.toml"), "w") as f: f.write("[package]\nname = 'db'\nversion = '1.0'\n")
    with open(os.path.join(db_dir, "main.aayu"), "w") as f: f.write("import models\n")
    
    # Models
    models_dir = os.path.join(test_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    with open(os.path.join(models_dir, "Aayu.toml"), "w") as f: f.write("[package]\nname = 'models'\nversion = '1.0'\n")
    with open(os.path.join(models_dir, "main.aayu"), "w") as f: f.write("import auth\n")
    
    loader = WorkspaceLoader(test_dir)
    loader.load()
    
    graph = ModuleGraph(loader)
    graph.build_graph()
    
    try:
        graph.kahn_topological_sort()
        assert False, "Should have thrown circular dependency error"
    except ValueError as e:
        msg = str(e)
        assert "Circular Dependency Detected" in msg
        assert "auth" in msg
        assert "db" in msg
        assert "models" in msg
        assert "auth imports db" in msg
        print("[OK] Circular Dependency Reporter passed!")

if __name__ == "__main__":
    test_topological_sort()
    test_circular_dependency()
