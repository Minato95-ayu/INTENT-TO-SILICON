from tools.package_manager.manager import PackageManager
import sys

def handle(args):
    if not args:
        print("Usage: aayu login <token>")
        sys.exit(1)
        
    pm = PackageManager()
    pm.login(args[0])
