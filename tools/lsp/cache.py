class SymbolCache:
    """Global symbol indexer to prevent scanning entire workspaces for Go To Definition."""
    
    def __init__(self):
        self.global_symbols = {}
        
    def index_workspace(self, root_uri: str):
        # Stub: Crawls the workspace files and extracts top-level symbols
        pass
        
    def get_symbol(self, name: str):
        return self.global_symbols.get(name)
