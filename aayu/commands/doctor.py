import sys
import os
import socket

def check(name, test_fn):
    try:
        result = test_fn()
        if result:
            print(f"[OK] {name}")
            return True
        else:
            print(f"[FAIL] {name}")
            return False
    except Exception as e:
        print(f"[FAIL] {name} (Error: {e})")
        return False

def handle(args):
    print("AAYU Doctor\n")
    
    all_ok = True
    
    # 1. Python
    def check_python():
        return sys.version_info >= (3, 11)
    all_ok &= check("Python (>=3.11)", check_python)
    
    # 2. Compiler
    def check_compiler():
        import aayu.compiler.lexer.lexer
        return True
    all_ok &= check("Compiler", check_compiler)
    
    # 3. VM
    def check_vm():
        import aayu.runtime.vm.vm
        return True
    all_ok &= check("VM", check_vm)
    
    # 4. Stdlib
    def check_stdlib():
        aayu_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.exists(os.path.join(aayu_dir, "runtime", "vm", "handlers"))
    all_ok &= check("Stdlib", check_stdlib)
    
    # 5. Templates
    def check_templates():
        aayu_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.exists(os.path.join(aayu_dir, "templates", "blank"))
    all_ok &= check("Templates", check_templates)
    
    # 6. Manifest
    def check_manifest():
        from aayu.package.manifest import AayuManifest
        manifest = AayuManifest()
        return manifest.exists()
    all_ok &= check("Manifest (in current project)", check_manifest)
    
    # 7. Port 3000 available
    def check_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', 3000)) != 0
    all_ok &= check("Port 3000 available", check_port)
    
    print("\n" + ("No problems found." if all_ok else "Some checks failed."))