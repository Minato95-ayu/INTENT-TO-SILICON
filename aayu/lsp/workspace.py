from .document import Document

class WorkspaceManager:
    def __init__(self):
        self.documents = {}

    def open_document(self, uri, text):
        doc = Document(uri, text)
        self.documents[uri] = doc
        return doc.get_diagnostics()

    def update_document(self, uri, text):
        if uri not in self.documents:
            return self.open_document(uri, text)
        doc = self.documents[uri]
        doc.update(text)
        return doc.get_diagnostics()
        
    def get_document(self, uri):
        return self.documents.get(uri)
