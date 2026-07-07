"""
=============================================================================
FILE: update_cli.py
PURPOSE: Updates CLI commands
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles updates cli commands.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os

with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\cli.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Replace do_install
import re
content = re.sub(r'def do_install\(package_name\):[\s\S]*?(?=def do_build\(intent_prompt\):)', '', content)

new_commands = '''
def do_install(package_name=None):
    from package_manager import AAYUPackageManager
    pm = AAYUPackageManager()
    pm.install(package_name)

def do_remove(package_name):
    from package_manager import AAYUPackageManager
    pm = AAYUPackageManager()
    pm.remove(package_name)

def do_update(package_name=None):
    from package_manager import AAYUPackageManager
    pm = AAYUPackageManager()
    pm.update(package_name)

def do_search(query):
    from package_manager import AAYUPackageManager
    pm = AAYUPackageManager()
    pm.search(query)

def do_publish():
    from package_manager import AAYUPackageManager
    pm = AAYUPackageManager()
    pm.publish()

def do_login():
    print("AAYU Registry Login (Mock)")
    print("Logged in successfully.")

def do_logout():
    print("AAYU Registry Logout")

def do_info():
    print("AAYU Package Information")

def do_graph():
    print("AAYU Dependency Graph")

def do_clean():
    import shutil
    if os.path.exists(".aayu/packages"):
        shutil.rmtree(".aayu/packages")
        print("Cleaned .aayu/packages")
'''

content = content.replace('def do_build(intent_prompt):', new_commands + '\ndef do_build_intent(intent_prompt):')

with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\cli.py', 'w', encoding='utf-8') as f:
    f.write(content)
