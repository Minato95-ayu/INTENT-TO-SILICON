import os
import sys
import distutils.ccompiler
from distutils.errors import CompileError, LinkError

def build_runtime():
    # Set paths
    native_dir = os.path.dirname(os.path.abspath(__file__))
    
    import datetime
    
    # Source files
    sources = [
        "metadata.c",
        "memory.c",
        "string.c",
        "array.c",
        "io.c",
        "panic.c",
        "math.c",
        "gc.c",
        "object.c"
    ]
    
    sources = [os.path.join(native_dir, src) for src in sources]
    
    if sys.platform == 'win32':
        sources.append(os.path.join(native_dir, "network/windows/network_windows.c"))
    elif sys.platform.startswith('linux'):
        sources.append(os.path.join(native_dir, "network/linux/network_linux.c"))
    elif sys.platform == 'darwin':
        sources.append(os.path.join(native_dir, "network/macos/network_macos.c"))

    # Create compiler
    compiler = distutils.ccompiler.new_compiler()
    
    # Define macros
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    macros = [
        ("AAYU_BUILD_COMPILER", f'"{compiler.compiler_type}"'),
        ("AAYU_BUILD_TIMESTAMP", f'"{timestamp}"'),
        ("AAYU_TARGET_TRIPLE", f'"{sys.platform}"')
    ]
    
    try:
        # Compile
        print("Compiling AAYU Native Runtime...")
        objects = compiler.compile(sources, output_dir=native_dir, macros=macros)
        
        # Link
        print("Linking AAYU Native Runtime...")
        
        extra_postargs = []
        if sys.platform == 'win32':
            # Force DLL creation if distutils forgets
            extra_postargs.append('/DLL')
            if compiler.compiler_type == 'msvc':
                extra_postargs.extend(['ws2_32.lib', 'Iphlpapi.lib'])
            else:
                extra_postargs.extend(['-lws2_32', '-liphlpapi'])
            output_libname = "aayu_runtime.dll"
        else:
            output_libname = "libaayu_runtime.so"
            
        compiler.link_shared_object(
            objects,
            output_libname,
            output_dir=native_dir,
            extra_postargs=extra_postargs
        )
        
        print(f"Successfully built {output_libname} shared library.")
        
    except (CompileError, LinkError) as e:
        print(f"Failed to build AAYU Native Runtime: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_runtime()
