"""
=============================================================================
FILE: test_resolver.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "prototype", "language"))

from workspace.workspace import Workspace

if __name__ == "__main__":
    ws = Workspace("mock_workspace")
    try:
        # Build returns the bytecode for the entry file, but we should actually execute the whole workspace
        # Wait, workspace.py build method compiles all files but returns only entry file bytecode.
        # We need to execute the dependencies first.
        print("Running build pipeline...")
        sorted_asts = ws.resolver.resolve("mock_workspace/src/main.aayu")
        for mod, ast in sorted_asts:
            print(f"Module {mod} statements: {ast.statements}")
        bytecodes = ws.build("mock_workspace/src/main.aayu")
        print("Build successful.")
        
        from aayu.runtime.vm.vm import VirtualMachine
        from aayu.runtime.memory.manager import MemoryManager
        
        memory = MemoryManager()
        vm = VirtualMachine(memory)
        
        for idx, bc in enumerate(bytecodes):
            vm.run(bc)
            
    except Exception as e:
        print(f"Error during resolution or build: {e}")
        import traceback
        traceback.print_exc()
