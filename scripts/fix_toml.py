"""
=============================================================================
FILE: fix_toml.py
PURPOSE: Fixes TOML configuration
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles fixes toml configuration.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os
import sys

def fix_package_manager():
    with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\package_manager.py', 'r') as f:
        content = f.read()

    new_write_toml = '''
    def _write_toml(self, path: str, data: Dict):
        # A simple recursive TOML writer for MVP
        def format_value(v):
            if isinstance(v, dict):
                items = []
                for kk, vv in v.items():
                    items.append(f"{kk} = {format_value(vv)}")
                return "{ " + ", ".join(items) + " }"
            elif isinstance(v, str):
                return f'"{v}"'
            elif isinstance(v, bool):
                return "true" if v else "false"
            elif v is None:
                return '""'
            else:
                return str(v)

        with open(path, "w", encoding="utf-8") as f:
            for key, value in data.items():
                if isinstance(value, dict) and key in ["dependencies", "packages", "versions"]:
                    if key == "versions":
                        for v_key, v_val in value.items():
                            f.write(f'\\n[versions."{v_key}"]\\n')
                            for meta_k, meta_v in v_val.items():
                                f.write(f'{meta_k} = {format_value(meta_v)}\\n')
                    else:
                        f.write(f"\\n[{key}]\\n")
                        for k, v in value.items():
                            f.write(f'{k} = {format_value(v)}\\n')
                else:
                    f.write(f'{key} = {format_value(value)}\\n')
'''

    import re
    content = re.sub(r'    def _write_toml\(self, path: str, data: Dict\):[\s\S]*?(?=    def _write_lock)', new_write_toml, content)

    with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\package_manager.py', 'w') as f:
        f.write(content)

fix_package_manager()
