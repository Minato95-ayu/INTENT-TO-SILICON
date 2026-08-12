import os
import sys
import shutil
import random
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aayu.compiler.workspace import WorkspaceLoader
from aayu.compiler.graph import ModuleGraph
from aayu.compiler.cache import IncrementalCache, BuildPlanner

def test_stress_architecture():
    print("Initializing Stress Test Environment...")
    test_dir = os.path.join(os.path.dirname(__file__), "stress_test_workspace")
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    MODULE_COUNT = 300
    
    # 1. Generate random DAG (no cycles yet)
    # To ensure it's a DAG, module `i` can only import from modules `j` where `j < i`.
    modules_imports = {}
    for i in range(MODULE_COUNT):
        num_imports = random.randint(0, min(10, i))
        if num_imports > 0 and i > 0:
            imports = random.sample(range(i), num_imports)
        else:
            imports = []
        modules_imports[i] = [f"mod_{j}" for j in imports]
        
    members = [f"mod_{i}" for i in range(MODULE_COUNT)]
    
    # 2. Write Aayu.toml and main.aayu for each module
    print(f"Generating {MODULE_COUNT} modules...")
    root_toml = f"""
    [package]
    name = "main"
    version = "1.0.0"
    [workspace]
    members = {members}
    """
    with open(os.path.join(test_dir, "Aayu.toml"), "w") as f: f.write(root_toml)
    with open(os.path.join(test_dir, "main.aayu"), "w") as f: f.write("") # empty root
    
    for i in range(MODULE_COUNT):
        mod_name = f"mod_{i}"
        mod_dir = os.path.join(test_dir, mod_name)
        os.makedirs(mod_dir)
        with open(os.path.join(mod_dir, "Aayu.toml"), "w") as f:
            f.write(f"[package]\nname = '{mod_name}'\nversion = '1.0'\n")
            
        imports_str = "\n".join([f"import {imp}" for imp in modules_imports[i]])
        with open(os.path.join(mod_dir, "main.aayu"), "w") as f:
            f.write(imports_str + "\n// code\n")

    # 3. Test Load and Graph Build
    print("Testing WorkspaceLoader & ModuleGraph Build...")
    start_time = time.time()
    loader = WorkspaceLoader(test_dir)
    loader.load()
    graph = ModuleGraph(loader)
    graph.build_graph()
    build_time = time.time() - start_time
    print(f"Graph Built in {build_time:.3f} seconds.")
    
    # 4. Kahn's Topological Sort
    print("Testing Kahn's Topological Sort (Stress)...")
    start_time = time.time()
    order = graph.kahn_topological_sort()
    sort_time = time.time() - start_time
    print(f"Sorted {len(order)} modules in {sort_time:.3f} seconds.")
    assert len(order) == MODULE_COUNT + 1 # +1 for root main
    
    # 5. Build Planner & Cache
    print("Testing Incremental Cache (Full Build)...")
    cache = IncrementalCache(test_dir)
    planner = BuildPlanner(graph, cache)
    order, actions = planner.plan()
    
    compile_count = sum(1 for a in actions.values() if a == "Compile")
    assert compile_count == MODULE_COUNT + 1
    
    # Mock compile
    for node in order:
        node.ast_hash = "AST_" + node.id
        node.compile_state = "Done"
        cache.update_module_cache(node)
    
    print("Testing Incremental Cache (Zero-Change Rebuild)...")
    graph2 = ModuleGraph(loader)
    graph2.build_graph()
    planner2 = BuildPlanner(graph2, cache)
    order2, actions2 = planner2.plan()
    
    skip_count = sum(1 for a in actions2.values() if a == "Skip")
    assert skip_count == MODULE_COUNT + 1, "Cache failed to skip unchanged modules"
    
    # 6. Test Circular Dependency Injection
    print("Testing Cycle Detection under Stress...")
    # Inject cycle: mod_10 imports mod_200, mod_200 imports mod_10 (but mod_200 already imported mod_10 likely)
    with open(os.path.join(test_dir, "mod_10", "main.aayu"), "a") as f:
        f.write("import mod_200\n")
        
    loader3 = WorkspaceLoader(test_dir)
    loader3.load()
    graph3 = ModuleGraph(loader3)
    graph3.build_graph()
    
    try:
        graph3.kahn_topological_sort()
        assert False, "Failed to detect injected cycle!"
    except ValueError as e:
        msg = str(e)
        assert "Circular Dependency Detected" in msg
        print("[OK] Cycle correctly isolated in massive graph!")
        
    print("\n==================================")
    print("STRESS TEST: PASSED")
    print("==================================")

if __name__ == "__main__":
    test_stress_architecture()
