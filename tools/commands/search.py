from tools.package_manager.manager import PackageManager
import sys

def handle(args):
    if not args:
        print("Usage: aayu search <query>")
        sys.exit(1)
        
    pm = PackageManager()
    pm.search(args[0])
