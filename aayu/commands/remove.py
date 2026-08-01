import sys
from aayu.package.manifest import AayuManifest

def handle(args):
    if len(args) < 1:
        print("Usage: aayu remove <package>")
        sys.exit(1)
        
    pkg_name = args[0]
    
    manifest = AayuManifest()
    if not manifest.exists():
        print("Error: No Aayu.toml found.")
        sys.exit(1)
        
    success = manifest.remove_dependency(pkg_name)
    if success:
        print(f"Removed {pkg_name} from Aayu.toml dependencies.")
    else:
        print(f"Package {pkg_name} not found in dependencies.")
        sys.exit(1)
