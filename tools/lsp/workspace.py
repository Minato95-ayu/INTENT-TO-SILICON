# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

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
