import sys

def handle(args):
    try:
        import pygls
    except ImportError:
        print("Error: LSP dependencies are not installed.")
        print("Run: pip install aayu-lang[lsp]")
        sys.exit(1)
        
    from aayu.lsp.server import start_server
    
    stdio = True
    if "--tcp" in args:
        stdio = False
        
    start_server(stdio=stdio)
