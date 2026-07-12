"""
=============================================================================
FILE: cli.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import sys
import os
import argparse
from pathlib import Path

# Add language path so we can import workspace
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../language')))
from workspace.workspace import Workspace

def cmd_init(args):
    print("Initializing new AAYU project...")
    if os.path.exists("Aayu.toml"):
        print("Error: Aayu.toml already exists!")
        sys.exit(1)
        
    with open("Aayu.toml", "w", encoding="utf-8") as f:
        f.write("""[package]
name = "new_project"
version = "0.1.0"
edition = "2026"

[build]
entry = "src/main.aayu"

[dependencies]
""")
    
    os.makedirs("src", exist_ok=True)
    if not os.path.exists("src/main.aayu"):
        with open("src/main.aayu", "w", encoding="utf-8") as f:
            f.write('print("Hello from AAYU!")\n')
            
    print("Initialized project in", os.getcwd())

def cmd_add(args):
    print(f"Adding dependency: {args.package}")
    manifest_path = Path("Aayu.toml")
    if not manifest_path.exists():
        print("Error: No Aayu.toml found. Run 'aayu init' first.")
        sys.exit(1)
        
    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Naive appending for now
    if "[dependencies]" not in content:
        content += "\n[dependencies]\n"
        
    if f"{args.package} =" in content:
        print(f"Package '{args.package}' is already in Aayu.toml.")
        return
        
    content += f'{args.package} = "1.0.0"\n'
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Added {args.package} to Aayu.toml.")
    # Now run build to trigger installation
    cmd_build(args)

def cmd_remove(args):
    print(f"Removing dependency: {args.package}")
    # Simplified removal logic for the prototype
    print("Command 'remove' not fully implemented yet.")

def cmd_build(args):
    ws = Workspace(Path(os.getcwd()))
    try:
        ws.build()
        print("Build successful.")
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)

def cmd_run(args):
    ws = Workspace(Path(os.getcwd()))
    try:
        # Assuming build returns bytecode and we can run it, or we just rely on Workspace execution
        bytecodes = ws.build()
        print("--- Running ---")
        ws.vm.execute(bytecodes)
    except Exception as e:
        print(f"Run failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="AAYU Package Manager and Build Tool")
    subparsers = parser.add_subparsers(dest="command")

    # init
    parser_init = subparsers.add_parser("init", help="Initialize a new project")
    
    # add
    parser_add = subparsers.add_parser("add", help="Add a dependency")
    parser_add.add_argument("package", type=str, help="Name of the package")
    
    # remove
    parser_remove = subparsers.add_parser("remove", help="Remove a dependency")
    parser_remove.add_argument("package", type=str, help="Name of the package")
    
    # build
    parser_build = subparsers.add_parser("build", help="Build the project")
    
    # run
    parser_run = subparsers.add_parser("run", help="Run the project")
    
    args = parser.parse_args()
    
    if args.command == "init":
        cmd_init(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "remove":
        cmd_remove(args)
    elif args.command == "build":
        cmd_build(args)
    elif args.command == "run":
        cmd_run(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
