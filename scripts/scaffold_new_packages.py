"""
=============================================================================
FILE: scaffold_new_packages.py
PURPOSE: Creates new package templates
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles creates new package templates.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os

packages = {
    "fs": {
        "methods": ["read_file", "write_file", "list_dir"],
        "desc": "File system operations"
    },
    "json": {
        "methods": ["parse", "stringify"],
        "desc": "JSON parsing and stringification"
    },
    "math": {
        "methods": ["sin", "cos", "floor", "ceil", "random"],
        "desc": "Standard mathematical functions"
    },
    "datetime": {
        "methods": ["now", "format"],
        "desc": "Date and time utilities"
    },
    "crypto": {
        "methods": ["sha256", "uuid"],
        "desc": "Cryptographic functions"
    }
}

base_dir = "official_packages"

for pkg, data in packages.items():
    pkg_dir = os.path.join(base_dir, f"aayu-{pkg}")
    os.makedirs(pkg_dir, exist_ok=True)
    
    # aayu.toml
    toml_path = os.path.join(pkg_dir, "aayu.toml")
    with open(toml_path, "w") as f:
        f.write(f"""[package]
name = "{pkg}"
version = "1.0.0"
description = "{data['desc']}"
author = "AAYU Official"

[dependencies]
""")

    # main.aayu
    aayu_path = os.path.join(pkg_dir, "main.aayu")
    with open(aayu_path, "w") as f:
        f.write(f"// AAYU Official Package: {pkg}\n")
        f.write(f"// {data['desc']}\n\n")
        
        for method in data['methods']:
            f.write(f"fn {method}() {{\n")
            f.write(f"    // Native implementation hooked in VM\n")
            f.write(f"}}\n\n")
            
    print(f"Scaffolded aayu-{pkg}")
