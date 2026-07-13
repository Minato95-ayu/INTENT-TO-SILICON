import sys
import os
import argparse
import importlib

class AAYUCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="AAYU Intent-to-Silicon Compiler & CLI",
            usage="aayu <command> [<args>]"
        )
        self.parser.add_argument("command", help="Command to run (new, run, build, test, etc.)")
        
    def execute(self):
        if len(sys.argv) < 2:
            self.parser.print_help()
            sys.exit(1)
            
        command = sys.argv[1]
        args = sys.argv[2:]
        
        if command in ["--help", "-h"]:
            self.parser.print_help()
            sys.exit(0)
            
        # Handle special flags
        if command in ["--version", "-v"]:
            command = "version"
            
        try:
            # Dynamically load the command module from tools.commands
            module = importlib.import_module(f"tools.commands.{command}")
            if hasattr(module, "handle"):
                module.handle(args)
            else:
                print(f"Error: Command module '{command}' is missing a handle() function.")
                sys.exit(1)
        except ModuleNotFoundError as e:
            if e.name == f"tools.commands.{command}":
                print(f"aayu: '{command}' is not a recognized command.")
                print("Run 'aayu --help' for usage.")
                sys.exit(1)
            else:
                # If the error is inside the command module, raise it
                raise

def main():
    cli = AAYUCLI()
    cli.execute()

if __name__ == "__main__":
    main()
