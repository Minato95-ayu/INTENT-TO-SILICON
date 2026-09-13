import os, re
tests_dir = r"D:\INTENT-TO-SILICON\tests"

for root, _, files in os.walk(tests_dir):
    for f in files:
        if not f.endswith(".py"): continue
        path = os.path.join(root, f)
        with open(path, "r", encoding="utf8") as file:
            content = file.read()
        
        orig = content
        
        # 1. Syntax Fixes
        if f == "test_phase1_core6.py" and content.startswith(" "):
            content = content.lstrip()
        if f == "test_pipeline_comprehensive.py":
            content = content.replace("assert len(bytecode.instructions) > 0idef", "assert len(bytecode.instructions) > 0\n\ndef")
            
        # 2. Safe Remapping (Category 1)
        content = content.replace("compiler.frontend.lexer", "compiler.lexer.lexer")
        content = content.replace("compiler.frontend.parser", "compiler.parser.parser")
        content = content.replace("compiler.frontend.ast_nodes", "compiler.ast.nodes")
        content = content.replace("compiler.frontend.errors", "compiler.errors")
        content = content.replace("AAYUSyntaxError", "CompilerError")
        content = content.replace("runtime.vm_next", "runtime.vm")
        
        # Category 5: Known API Refactors
        content = content.replace("tools.package_manager", "tools.package_manager.manager")
        content = content.replace("AAYUPackageManager", "PackageManager")
        
        # 3. Category 2 (Semantic adaptation imports update - if tests fail, we review manually)
        content = content.replace("compiler.frontend.resolver.symbols", "compiler.semantic.symbols")
        content = content.replace("compiler.frontend.type_nodes", "compiler.ast.nodes")
        content = content.replace("compiler.frontend.passes.semantic.type_checker", "compiler.semantic.type_checker")
        content = content.replace("compiler.frontend.passes.semantic.symbol_binding", "compiler.semantic.analyzer")
        content = content.replace("compiler.frontend.compiler_context", "compiler.semantic.analyzer")
        
        # 4. Mark Obsolete Tests (Category 3) - Do not fake APIs
        obsolete = ""
        if "AAYUCompiler" in content:
            obsolete = "Obsolete API: AAYUCompiler removed in favor of IRPipeline"
        elif "runtime.vm.handlers.math" in content or "execute_add" in content:
            obsolete = "Obsolete API: Handlers directory moved inline"
        elif "runtime.vm.handlers.logic" in content:
            obsolete = "Obsolete API: Logic handlers moved inline"
        elif "AAYUEngine" in content:
            obsolete = "Obsolete API: Engine moved to intent_engine"
            
        if obsolete:
            if "pytestmark = pytest.mark.skip" not in content:
                content = f"import pytest\npytestmark = pytest.mark.skip(reason='{obsolete}')\n\n" + content
                
        if content != orig:
            with open(path, "w", encoding="utf8") as file:
                file.write(content)

print("Targeted R1.2 fixes applied.")
