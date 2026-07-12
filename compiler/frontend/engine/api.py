"""
=============================================================================
FILE: api.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import json
import sys

# Ensure prototype is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
prototype_dir = os.path.dirname(current_dir)
if prototype_dir not in sys.path:
    sys.path.insert(0, prototype_dir)
aayu_lang_dir = os.path.join(prototype_dir, "language")
if aayu_lang_dir not in sys.path:
    sys.path.insert(0, aayu_lang_dir)

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.ir_generator import generate_ir
from compiler.frontend.compiler import AAYUCompiler
from runtime.vm.vm import VirtualMachine

class AAYUProject:
    def __init__(self, source: str, filepath: str = "main.aayu"):
        self.source = source
        self.filepath = filepath
        self.ast = None
        self.ir_data = None
        self.bytecode = None
        
    def validate(self):
        """Lexes and parses the source to check for syntax errors."""
        lexer = Lexer(self.source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename=self.filepath)
        self.ast = parser.parse()
        return self.ast

    def compile(self):
        """Compiles the AST to AAYU Bytecode and generates Architecture IR."""
        if not self.ast:
            self.validate()
            
        # 1. Architecture IR for generators
        ir_json_str = generate_ir(self.ast)
        self.ir_data = json.loads(ir_json_str)
        
        # 2. Bytecode for VM
        compiler = AAYUCompiler()
        self.bytecode = compiler.compile(self.ast)
        return self.bytecode
        
    def run(self):
        """Executes the compiled bytecode in the AAYU Virtual Machine."""
        if not self.bytecode:
            self.compile()
            
        vm = VirtualMachine()
        return vm.run(self.bytecode)
        
    def generate(self, targets=None, out_dir="generated_project"):
        """Generates production software code using targeted code generators."""
        if not self.ir_data:
            self.compile()
            
        if targets is None:
            # Auto-select based on project intent if no targets specified
            from target_engine.scorer import select_target
            target_plan_json = select_target(self.ir_data)
            target_plan = json.loads(target_plan_json)
            targets = target_plan.get("generators", [])
            
        # Normalize target names
        normalized_targets = []
        for t in targets:
            if "react" in t: normalized_targets.append("react")
            if "fastapi" in t: normalized_targets.append("fastapi")
            if "postgres" in t or "postgresql" in t: normalized_targets.append("postgres")
            if "orchestrator" in t: normalized_targets.append("orchestrator")
            
        if "react" in normalized_targets:
            from generators.react.generator import ReactGenerator
            ReactGenerator(self.ir_data, os.path.join(out_dir, "frontend")).generate()
            
        if "fastapi" in normalized_targets:
            from generators.fastapi.generator import FastAPIGenerator
            FastAPIGenerator(self.ir_data, os.path.join(out_dir, "backend")).generate()
            
        if "postgres" in normalized_targets:
            from generators.postgres.generator import PostgresGenerator
            PostgresGenerator(self.ir_data, os.path.join(out_dir, "database")).generate()
            
        # Orchestrator always runs if other targets run, unless explicitly excluded, but we'll include it manually or auto
        # To be safe, if we generate backend/frontend, we orchestrate
        from generators.orchestrator.generator import OrchestratorGenerator
        OrchestratorGenerator(self.ir_data, out_dir).generate()
        
        return True


class AAYUEngine:
    """The central Engine API for AAYU ecosystem."""
    
    def load(self, filepath: str) -> AAYUProject:
        """Loads an AAYU project from a file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        return AAYUProject(source, filepath=filepath)
        
    def load_source(self, source: str) -> AAYUProject:
        """Loads an AAYU project directly from source code."""
        return AAYUProject(source, filepath="<memory>")
