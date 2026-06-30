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
        
        from runtime.vm.vm import VirtualMachine
        from runtime.memory.manager import MemoryManager
        
        memory = MemoryManager()
        vm = VirtualMachine(memory)
        
        for idx, bc in enumerate(bytecodes):
            vm.run(bc)
            
    except Exception as e:
        print(f"Error during resolution or build: {e}")
        import traceback
        traceback.print_exc()
