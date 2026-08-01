from lsprotocol.types import Hover, MarkupContent, MarkupKind

class HoverProvider:
    def __init__(self, workspace):
        self.workspace = workspace

    def get_hover(self, uri, position):
        doc = self.workspace.get_document(uri)
        if not doc:
            return None
        # Basic mock hover for v1
        return Hover(contents=MarkupContent(kind=MarkupKind.Markdown, value="**AAYU Symbol**\n\nPart of native ecosystem."))
