# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

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
