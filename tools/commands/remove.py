from tools.package_manager.manager import PackageManager
import sys

def handle(args):
    if not args:
        print("Usage: aayu remove <package>")
        sys.exit(1)
        
    pm = PackageManager()
    pm.remove(args[0])
