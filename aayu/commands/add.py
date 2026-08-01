import sys
from aayu.package.manifest import AayuManifest

def handle(args):
    if len(args) < 1:
        print("Usage: aayu add <package> [version]")
        sys.exit(1)
        
    pkg_name = args[0]
    version = args[1] if len(args) > 1 else "^1.0.0"
    
    manifest = AayuManifest()
    if not manifest.exists():
        print("Error: No Aayu.toml found. Run 'aayu init' first.")
        sys.exit(1)
        
    success = manifest.add_dependency(pkg_name, version)
    if success:
        print(f"Added {pkg_name} v{version} to Aayu.toml dependencies.")
    else:
        sys.exit(1)
