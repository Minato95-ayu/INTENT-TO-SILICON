from lsprotocol.types import CompletionList, CompletionItem, CompletionItemKind

class CompletionProvider:
    def __init__(self, workspace):
        self.workspace = workspace
        self.keywords = ["app", "page", "model", "task", "run", "let", "insert", "find", "respond", "title", "text", "end"]
        self.types = ["Int", "String", "Bool", "Float"]

    def get_completions(self, uri, position):
        items = []
        for kw in self.keywords:
            items.append(CompletionItem(label=kw, kind=CompletionItemKind.Keyword))
        for t in self.types:
            items.append(CompletionItem(label=t, kind=CompletionItemKind.Class))
        return CompletionList(is_incomplete=False, items=items)
