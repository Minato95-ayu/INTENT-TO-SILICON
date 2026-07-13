from tools.package_manager.manager import PackageManager

def handle(args):
    pm = PackageManager()
    
    if not args:
        pm.install()
    else:
        pkg = args[0]
        if ":" in pkg:
            # e.g., github:user/repo
            name = pkg.split("/")[-1]
            pm.install(name, source=pkg)
        else:
            pm.install(pkg)
