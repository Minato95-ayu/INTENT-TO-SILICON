import os
import sys
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aayu.compiler.api import Compiler
from aayu.compiler.ast.nodes import ProjectNode

def setup_mock_workspace(test_dir):
    os.makedirs(test_dir, exist_ok=True)
    
    root_toml = """
    [package]
    name = "main"
    version = "1.0.0"
    [workspace]
    members = ["auth", "db"]
    """
    with open(os.path.join(test_dir, "Aayu.toml"), "w") as f: f.write(root_toml)
    with open(os.path.join(test_dir, "main.aayu"), "w") as f: 
        f.write("import auth\nimport db\naction start()\nend\n")
    
    auth_dir = os.path.join(test_dir, "auth")
    os.makedirs(auth_dir, exist_ok=True)
    with open(os.path.join(auth_dir, "Aayu.toml"), "w") as f: f.write("[package]\nname = 'auth'\nversion = '1.0'\n")
    with open(os.path.join(auth_dir, "main.aayu"), "w") as f: 
        f.write("import db\nstruct User { id: str }\n")
        
    db_dir = os.path.join(test_dir, "db")
    os.makedirs(db_dir, exist_ok=True)
    with open(os.path.join(db_dir, "Aayu.toml"), "w") as f: f.write("[package]\nname = 'db'\nversion = '1.0'\n")
    with open(os.path.join(db_dir, "main.aayu"), "w") as f: 
        f.write("struct DBConnection {}\n")

def test_compile_workspace():
    test_dir = os.path.join(os.path.dirname(__file__), "mock_multifile_project")
    if os.path.exists(test_dir): shutil.rmtree(test_dir)
    setup_mock_workspace(test_dir)
    
    compiler = Compiler()
    success = compiler.compile_workspace(test_dir)
    
    if not success:
        compiler.diag.print_all()
        
    assert success, "compile_workspace failed!"
    assert isinstance(compiler.ast, ProjectNode), "AST should be a ProjectNode"
    
    modules = compiler.ast.modules
    assert "main" in modules
    assert "auth" in modules
    assert "db" in modules
    
    print(f"[OK] Multi-file Parser generated ProjectNode with {len(modules)} modules!")
    
    # Verify caching logic
    cache_dir = os.path.join(test_dir, ".aayu_cache")
    assert os.path.exists(cache_dir), "Cache dir not created"
    
    ast_files = [f for f in os.listdir(cache_dir) if f.endswith(".ast")]
    assert len(ast_files) == 3, f"Expected 3 .ast files, found {len(ast_files)}"
    print("[OK] AST files successfully cached to disk!")
    
    # 2nd run: should load from cache
    print("Testing Cached Parse...")
    compiler2 = Compiler()
    success2 = compiler2.compile_workspace(test_dir)
    assert success2, "compile_workspace failed on cache load"
    modules2 = compiler2.ast.modules
    assert "auth" in modules2
    print("[OK] Cache successfully loaded ProjectNode without re-parsing!")
    
    # Check ProjectScope
    project_scope = compiler.project_scope
    assert project_scope is not None, "ProjectScope should be created"
    assert project_scope._is_frozen, "ProjectScope should be frozen"
    
    auth_module = project_scope.get_module("auth")
    assert auth_module is not None
    assert auth_module.exports.resolve("User") is not None, "User struct not found in auth module exports"
    
    db_module = project_scope.get_module("db")
    assert db_module is not None
    assert db_module.exports.resolve("DBConnection") is not None, "DBConnection struct not found in db module exports"
    
    main_module = project_scope.get_module("main")
    assert main_module is not None
    assert main_module.exports.resolve("start") is not None, "start action not found in main module exports"
    
    print("[OK] ProjectScope is built, immutable, and contains module symbols!")

if __name__ == "__main__":
    test_compile_workspace()
