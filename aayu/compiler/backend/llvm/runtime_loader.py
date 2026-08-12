import os
import sys
import ctypes

try:
    import llvmlite.binding as llvm
    LLVMLITE_AVAILABLE = True
except ImportError:
    LLVMLITE_AVAILABLE = False

COMPILER_ABI_MAJOR = 1
COMPILER_ABI_MINOR = 0
COMPILER_ABI_PATCH = 0

class RuntimeLoader:
    """
    Single authority for AAYU Native Runtime discovery, verification, and loading.
    """
    
    @staticmethod
    def initialize():
        if not LLVMLITE_AVAILABLE:
            raise RuntimeError("llvmlite is not installed. Cannot load native runtime.")
            
        # 1. Locate Runtime
        native_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "runtime", "native"
        )
        
        if sys.platform == 'win32':
            runtime_path = os.path.join(native_dir, "aayu_runtime.dll")
        else:
            runtime_path = os.path.join(native_dir, "libaayu_runtime.so")
            
        if not os.path.exists(runtime_path):
            print(f"WARNING: AAYU Native Runtime not found at {runtime_path}. Native calls will fail during JIT.")
            return False
            
        # 2. Verify ABI using ctypes before permanent loading
        try:
            lib = ctypes.CDLL(runtime_path)
            
            # Extract metadata
            lib.aayu_runtime_abi_major.restype = ctypes.c_int
            lib.aayu_runtime_abi_minor.restype = ctypes.c_int
            lib.aayu_runtime_abi_patch.restype = ctypes.c_int
            lib.aayu_runtime_version.restype = ctypes.c_char_p
            lib.aayu_compiler_name.restype = ctypes.c_char_p
            lib.aayu_build_timestamp.restype = ctypes.c_char_p
            
            runtime_major = lib.aayu_runtime_abi_major()
            runtime_minor = lib.aayu_runtime_abi_minor()
            runtime_patch = lib.aayu_runtime_abi_patch()
            
            runtime_version = lib.aayu_runtime_version().decode('utf-8')
            compiler_name = lib.aayu_compiler_name().decode('utf-8')
            build_timestamp = lib.aayu_build_timestamp().decode('utf-8')
            
            # Semantic Version Check
            if runtime_major != COMPILER_ABI_MAJOR:
                raise RuntimeError(f"ABI Major mismatch: Compiler expects {COMPILER_ABI_MAJOR}.x.x, but Runtime is {runtime_major}.{runtime_minor}.{runtime_patch}")
                
            if runtime_minor != COMPILER_ABI_MINOR:
                print(f"WARNING: ABI Minor mismatch: Compiler expects {COMPILER_ABI_MAJOR}.{COMPILER_ABI_MINOR}.x, Runtime is {runtime_major}.{runtime_minor}.{runtime_patch}")
                
            # Log Diagnostics (Disabled by default, can be turned on via verbose flag in the future)
            # print(f"Loaded AAYU Native Runtime v{runtime_version} (ABI {runtime_major}.{runtime_minor}.{runtime_patch})")
            # print(f"Runtime Built with: {compiler_name} on {build_timestamp}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to load and verify AAYU Native Runtime: {e}")
            
        # 3. Load Permanently into LLVM Context
        llvm.load_library_permanently(runtime_path)
        return True
