import sys
from aayu.package.manifest import AayuManifest

def handle(args):
    manifest = AayuManifest()
    if not manifest.exists():
        print("Error: No Aayu.toml found.")
        sys.exit(1)
        
    deps = manifest.get_dependencies()
    name = manifest.get_package_name()
    
    print(f"Dependencies for {name}:")
    if not deps:
        print("  (No dependencies)")
    else:
        for pkg, ver in deps.items():
            print(f"  - {pkg}: {ver}")
