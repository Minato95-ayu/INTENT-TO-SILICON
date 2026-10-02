import os
import sys
from .compiler import BuilderCompiler
from .asset_manager import AssetManager
from .manifest import Manifest
from .targets.windows import WindowsTarget
from .targets.linux import LinuxTarget
from .targets.macos import MacTarget
from .targets.web import WebTarget

class Builder:
    def __init__(self, mode="release"):
        self.mode = mode
        self.compiler = BuilderCompiler(mode)
        self.assets = AssetManager()
        self.manifest = Manifest()
        
    def build(self, target: str):
        print(f"[Builder] Starting {self.mode.upper()} build for target: {target.upper()}")
        
        # 1. Compile AAYU AST/Bytecode
        bytecode, ast = self.compiler.compile("main.aayu")
        
        # 2. Prepare Assets
        self.assets.bundle()
        
        # 3. Generate Native Package
        if target == "windows":
            WindowsTarget().build(bytecode, self.assets)
        elif target == "linux":
            LinuxTarget().build(bytecode, self.assets)
        elif target == "macos":
            MacTarget().build(bytecode, self.assets)
        elif target == "web":
            WebTarget().build(ast, self.assets)
        else:
            print(f"[Builder] Unsupported target: {target}")
            sys.exit(1)
            
        print(f"[Builder] Successfully generated {target} package.")
