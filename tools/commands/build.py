import sys
from tools.builder import Builder

def handle(args):
    # Parse args
    target = "windows"
    mode = "release"
    
    # Parse explicit targets
    if "--target" in args:
        idx = args.index("--target")
        if idx + 1 < len(args):
            target = args[idx + 1]
            
    # Parse modes
    if "--debug" in args:
        mode = "debug"
    if "--profile" in args:
        mode = "profile"
        
    builder = Builder(mode=mode)
    builder.build(target)
