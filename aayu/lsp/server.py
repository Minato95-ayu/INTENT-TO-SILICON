from pygls.lsp.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_HOVER,
    TEXT_DOCUMENT_DEFINITION,
    DidOpenTextDocumentParams,
    DidChangeTextDocumentParams,
    CompletionParams,
    HoverParams,
    DefinitionParams,
    Hover,
    CompletionList,
    CompletionItem,
    CompletionItemKind,
    Location
)
from .workspace import WorkspaceManager
from .completion import CompletionProvider
from .hover import HoverProvider
from .definition import DefinitionProvider

server = LanguageServer("aayu-lsp", "v1.0")
workspace = WorkspaceManager()
completion_provider = CompletionProvider(workspace)
hover_provider = HoverProvider(workspace)
definition_provider = DefinitionProvider(workspace)

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls, params: DidOpenTextDocumentParams):
    diagnostics = workspace.open_document(params.text_document.uri, params.text_document.text)
    ls.publish_diagnostics(params.text_document.uri, diagnostics)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    diagnostics = workspace.update_document(params.text_document.uri, params.content_changes[0].text)
    ls.publish_diagnostics(params.text_document.uri, diagnostics)

@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(ls, params: CompletionParams):
    return completion_provider.get_completions(params.text_document.uri, params.position)

@server.feature(TEXT_DOCUMENT_HOVER)
def hover(ls, params: HoverParams):
    return hover_provider.get_hover(params.text_document.uri, params.position)

@server.feature(TEXT_DOCUMENT_DEFINITION)
def goto_definition(ls, params: DefinitionParams):
    return definition_provider.get_definition(params.text_document.uri, params.position)

def start_server(stdio=True):
    if stdio:
        server.start_io()
    else:
        server.start_tcp("127.0.0.1", 2087)
