import os
import sys
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aayu.compiler.workspace import WorkspaceLoader
from aayu.compiler.graph import ModuleGraph
from aayu.compiler.cache import IncrementalCache, BuildPlanner

def setup_mock_project(test_dir):
    os.makedirs(test_dir, exist_ok=True)
    
    root_toml = """
    [package]
    name = "main"
    version = "1.0.0"
    [workspace]
    members = ["auth"]
    """
    with open(os.path.join(test_dir, "Aayu.toml"), "w") as f: f.write(root_toml)
    with open(os.path.join(test_dir, "main.aayu"), "w") as f: f.write("import auth\n")
    
    auth_dir = os.path.join(test_dir, "auth")
    os.makedirs(auth_dir, exist_ok=True)
    with open(os.path.join(auth_dir, "Aayu.toml"), "w") as f: f.write("[package]\nname = 'auth'\nversion = '1.0'\n")
    with open(os.path.join(auth_dir, "main.aayu"), "w") as f: f.write("// auth\n")

def test_cache_and_planner():
    test_dir = os.path.join(os.path.dirname(__file__), "mock_cache_project")
    if os.path.exists(test_dir): shutil.rmtree(test_dir)
    setup_mock_project(test_dir)
    
    # 1st Run: Should compile everything
    loader = WorkspaceLoader(test_dir)
    loader.load()
    graph = ModuleGraph(loader)
    graph.build_graph()
    
    cache = IncrementalCache(test_dir)
    planner = BuildPlanner(graph, cache)
    
    order, actions = planner.plan()
    assert actions["auth"] == "Compile"
    assert actions["main"] == "Compile"
    
    # Simulate compilation completing and saving state
    for node in order:
        node.ast_hash = "mock_ast_hash"
        node.compile_state = "Done"
        cache.update_module_cache(node)
        
    cache.generate_build_manifest(graph, 15.0, 0, 0)
    assert os.path.exists(os.path.join(test_dir, "build_manifest.json"))
    
    # 2nd Run: Unmodified, should skip everything
    graph2 = ModuleGraph(loader)
    graph2.build_graph()
    planner2 = BuildPlanner(graph2, cache)
    order2, actions2 = planner2.plan()
    assert actions2["auth"] == "Skip"
    assert actions2["main"] == "Skip"
    
    # 3rd Run: Modify auth, main should ALSO recompile due to dep_hash
    with open(os.path.join(test_dir, "auth", "main.aayu"), "w") as f:
        f.write("// changed auth\n")
        
    graph3 = ModuleGraph(loader)
    graph3.build_graph()
    planner3 = BuildPlanner(graph3, cache)
    order3, actions3 = planner3.plan()
    
    assert actions3["auth"] == "Compile", "Auth changed directly"
    assert actions3["main"] == "Compile", "Main should recompile because its dependency changed!"
    
    print("[OK] Incremental Cache and Build Planner passed!")

if __name__ == "__main__":
    test_cache_and_planner()
