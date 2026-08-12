import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aayu.compiler.api import Compiler
from aayu.compiler.errors import DiagnosticSeverity
from aayu.compiler.semantic.types import StructType, EnumType

def test_cross_module_types():
    files = {
        "core.models": """
        struct Point {
            x: Int
            y: Int
        }
        
        enum Status {
            Active,
            Inactive
        }
        
        fn getStatus() -> Status {
            return Status.Active
        }
        """,
        "main": """
        import core
        
        fn main() {
            let p: core.Point = core.Point { x: 10, y: 20 }
            let s: core.Status = core.getStatus()
            
            if (s == core.Status.Active) {
                print("Active")
            }
        }
        """
    }

    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    try:
        # Root Workspace
        with open(os.path.join(temp_dir, "Aayu.toml"), "w") as f:
            f.write('[package]\nname = "main"\nversion = "1.0"\n[workspace]\nmembers = ["core"]\n')
        with open(os.path.join(temp_dir, "main.aayu"), "w") as f:
            f.write(files["main"])
            
        # Core Module
        core_dir = os.path.join(temp_dir, "core")
        os.makedirs(core_dir)
        with open(os.path.join(core_dir, "Aayu.toml"), "w") as f:
            f.write('[package]\nname = "core"\nversion = "1.0"\n')
        with open(os.path.join(core_dir, "main.aayu"), "w") as f:
            f.write(files["core.models"])
            
        from aayu.compiler.api import Compiler
        compiler = Compiler()
        success = compiler.compile_workspace(temp_dir)
        
        has_errors = not success
        if has_errors:
            for d in compiler.diag.diagnostics:
                if d.severity == DiagnosticSeverity.ERROR:
                    print(f"[ERROR] {d.message} (span: {d.span})")
            assert False, "Cross module type resolution failed"
            
        print("[OK] Cross module types successfully resolved!")
        
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    test_cross_module_types()
