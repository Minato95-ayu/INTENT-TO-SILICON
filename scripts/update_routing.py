"""
=============================================================================
FILE: update_routing.py
PURPOSE: Updates routing system
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles updates routing system.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os
import re

with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\cli.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Let's replace the routing block at the end.
# We'll just append our new handlers into the main() function or block.

new_routing = '''
    elif cmd == "remove":
        if len(sys.argv) < 3:
            print("Error: Please provide a package name. Example: aayu remove auth")
        else:
            do_remove(sys.argv[2])
    elif cmd == "update":
        pkg = sys.argv[2] if len(sys.argv) >= 3 else None
        do_update(pkg)
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Error: Please provide a search query.")
        else:
            do_search(sys.argv[2])
    elif cmd == "publish":
        do_publish()
    elif cmd == "login":
        do_login()
    elif cmd == "logout":
        do_logout()
    elif cmd == "info":
        do_info()
    elif cmd == "graph":
        do_graph()
    elif cmd == "clean":
        do_clean()
'''

content = content.replace('    elif cmd == "build":\n        do_build()', new_routing + '\n    elif cmd == "build":\n        do_build()')

with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\cli.py', 'w', encoding='utf-8') as f:
    f.write(content)
