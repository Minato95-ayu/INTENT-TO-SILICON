from .document import Document

class Workspace:
    """Manages the virtual file system, caching active Document objects."""
    
    def __init__(self):
        self.documents = {}
        
    def did_open(self, msg):
        uri = msg["params"]["textDocument"]["uri"]
        text = msg["params"]["textDocument"]["text"]
        version = msg["params"]["textDocument"].get("version", 1)
        self.documents[uri] = Document(uri, text)
        self.documents[uri].version = version

    def did_change(self, msg):
        uri = msg["params"]["textDocument"]["uri"]
        version = msg["params"]["textDocument"].get("version")
        
        # In a real sync we handle incremental changes, but we specified Full sync for MVP
        if "contentChanges" in msg["params"] and len(msg["params"]["contentChanges"]) > 0:
            text = msg["params"]["contentChanges"][0].get("text")
            if text is not None and uri in self.documents:
                self.documents[uri].update(text, version)
                
    def get_document(self, uri: str) -> Document:
        return self.documents.get(uri)
