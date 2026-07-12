"""
===============================================================================
AAYU Compiler - Package & Workspace Manager

Purpose:
    Projects, Modules aur 'aayu.mod' files ko load aur resolve karta hai.

Pipeline:
    Memory Manager
        ↓
    Package Manager ← (Current File)

Ye file kyun important hai?
    Bade projects multiple files me hote hain. Ye file ensure karti hai ki 'import utils' likhne par sahi file load ho.

Difficulty:
    ⭐⭐ (Medium)

Recommended Reading Order:
    9. runtime/memory/manager.py
    10. workspace/workspace.py (You are here)
    11. brainos/orchestrator.py
===============================================================================
"""
import os
from pathlib import Path
from typing import Dict, List, Optional
from compiler.frontend.compiler import AAYUCompiler
from compiler.frontend.ir import Bytecode
from runtime.vm.vm import VirtualMachine

class Workspace:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        
        # We will import Resolver dynamically or later to avoid circular imports if needed
        from compiler.frontend.resolver.resolver import Resolver
        self.resolver = Resolver(self)
        
        # We need lowering and optimizer passes too
        from compiler.frontend.passes.lowering import LoweringPass
        self.lowering_pass = LoweringPass()
        
        from compiler.frontend.resolver.symbols import SymbolTable, ScopeType
        self.builtin_table = SymbolTable("builtins", ScopeType.BUILTIN)
        # TODO: populate builtins (print, list_append, etc.)
        
        self.compiler = AAYUCompiler()
        
    def build(self, entry_file: Optional[str] = None):
        print("Running build pipeline...")
        
        # 1. Locate and parse Aayu.toml
        from manifest.lexer import ManifestLexer
        from manifest.parser import ManifestParser
        from manifest.validator import ManifestValidator
        from compiler.frontend.compiler_context import CompilerContext, Diagnostics
        import os
        
        manifest_path = self.root_path / "Aayu.toml"
        temp_diagnostics = Diagnostics()
        manifest_obj = None
        
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                source = f.read()
            try:
                lexer = ManifestLexer(source)
                tokens = lexer.tokenize()
                parser = ManifestParser(tokens)
                ast_doc = parser.parse()
                validator = ManifestValidator(temp_diagnostics, str(manifest_path))
                manifest_obj = validator.validate(ast_doc)
            except Exception as e:
                temp_diagnostics.error(f"Manifest parse error: {e}", str(manifest_path))
        else:
            temp_diagnostics.error("Missing Aayu.toml manifest", str(manifest_path))
            
        if temp_diagnostics.has_errors():
            temp_diagnostics.print_all()
            raise Exception("Workspace startup failed due to manifest errors")
            
        # Ensure dependencies are installed via PackageManager
        from package.manager import PackageManager
        from package.registry import LocalRegistry
        
        if manifest_obj:
            registry = LocalRegistry(os.path.join(self.root_path, "mock_registry"))
            packages_dir = os.path.join(self.root_path, "packages")
            package_manager = PackageManager(temp_diagnostics, registry, packages_dir)
            if not package_manager.ensure_dependencies(manifest_obj):
                temp_diagnostics.print_all()
                raise Exception("Workspace startup failed due to dependency errors")
            
        if not entry_file:
            if manifest_obj and manifest_obj.build and manifest_obj.build.entry:
                entry_file = os.path.join(self.root_path, manifest_obj.build.entry)
            else:
                raise Exception("No entry file provided and no [build] entry found in manifest")
                
        # 2. Resolve and parse all files, returning a topologically sorted list of ASTs
        sorted_asts = self.resolver.resolve(entry_file)
        
        # Create CompilerContext and PassManager
        from compiler.frontend.passes.manager import PassManager
        from compiler.frontend.passes.semantic.module_resolver import ModuleResolverPass
        from compiler.frontend.passes.semantic.import_binding import ImportBindingPass
        from compiler.frontend.passes.semantic.scope_builder import ScopeBuilderPass
        from compiler.frontend.passes.semantic.symbol_binding import SymbolBindingPass
        from compiler.frontend.passes.semantic.export_validation import ExportValidationPass
        from compiler.frontend.passes.semantic.semantic_validation import SemanticValidationPass
        from compiler.frontend.passes.semantic.type_checker import TypeCheckerPass
        from workspace.cache import IncrementalCache
        
        cache = IncrementalCache(os.path.dirname(os.path.abspath(entry_file)))
        
        # Note: We need module_graph in context. self.resolver has module_graph.
        context = CompilerContext(workspace=self, module_graph=self.resolver.graph, cache=cache, manifest=manifest_obj)
        context.diagnostics.diagnostics.extend(temp_diagnostics.diagnostics)
        
        pass_manager = PassManager()
        pass_manager.add_pass(ModuleResolverPass())
        pass_manager.add_pass(ScopeBuilderPass())
        pass_manager.add_pass(ImportBindingPass())
        pass_manager.add_pass(SymbolBindingPass())
        pass_manager.add_pass(ExportValidationPass())
        pass_manager.add_pass(SemanticValidationPass())
        pass_manager.add_pass(TypeCheckerPass())
        
        from compiler.frontend.passes.optimizer import StaticOptimizerPass
        pass_manager.add_pass(StaticOptimizerPass())
        
        # 2. Semantic Analysis per module in topological order
        bytecodes = []
        lowered_asts = []
        
        for mod_name, ast in sorted_asts:
            filepath = self.resolver.module_paths.get(mod_name, "")
            
            # Setup context
            context.asts[mod_name] = ast
            from compiler.frontend.resolver.symbols import SymbolTable, ScopeType
            mod_table = SymbolTable(mod_name, ScopeType.MODULE, self.builtin_table)
            context.symbol_tables[mod_name] = mod_table
            
        for mod_name, ast in sorted_asts:
            filepath = self.resolver.module_paths.get(mod_name, "")
            context.current_module = mod_name
            
            # Note: For incremental cache, we could check if up_to_date here.
            # But we must run semantic passes to populate symbol tables for dependents.
            # In a true incremental system, symbol tables would be deserialized from cache.
            # For Phase 3.3, we'll still run the frontend passes but cache the bytecode.
            
            success = pass_manager.run(context)
            if not success:
                context.diagnostics.print_all()
                raise Exception(f"Compilation failed for module {mod_name}")
                
            # Lowering
            lowered = self.lowering_pass.lower(ast)
            lowered_asts.append((mod_name, lowered))
            
            # Compile
            compiler = AAYUCompiler(filename=mod_name)
            compiler.visit(lowered)
            bytecodes.append(compiler.bytecode)
            
            # Update cache
            # In real system, we extract exports and dependencies
            deps = list(self.resolver.graph.dependencies.get(mod_name, []))
            cache.update_module(mod_name, filepath, deps, [], "")
            
        cache.save()
        print("Build successful.")
        return bytecodes

    def run(self, entry_file: str):
        bytecodes = self.build(entry_file)
        vm = VirtualMachine()
        for bytecode in bytecodes:
            vm.run(bytecode)
