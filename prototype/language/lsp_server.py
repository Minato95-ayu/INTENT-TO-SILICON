from pygls.lsp.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    DidOpenTextDocumentParams,
    DidChangeTextDocumentParams,
    Diagnostic,
    DiagnosticSeverity,
    Position,
    Range,
)

import sys
import os
# Add prototype to sys.path so we can import aayu_language modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from prototype.aayu_language.lexer import Lexer
from prototype.aayu_language.parser import Parser
from prototype.aayu_language.errors import AAYUError

server = LanguageServer("aayu-lsp", "v1.0")

def validate_aayu_document(ls: LanguageServer, uri: str, text: str):
    diagnostics = []

    try:
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parser.parse()
    except AAYUError as e:
        # line and column are 1-indexed in our errors, but 0-indexed in LSP Position
        line = max(0, e.line - 1)
        col = max(0, e.column - 1)

        msg = e.message
        if e.hint:
            msg += f"\nHint: {e.hint}"

        diagnostics.append(
            Diagnostic(
                range=Range(
                    start=Position(line=line, character=col),
                    end=Position(line=line, character=col + 5), # highlight next 5 chars
                ),
                message=msg,
                severity=DiagnosticSeverity.Error,
                source="AAYU Parser"
            )
        )
    except Exception as e:
        # Fallback for unexpected compiler crashes
        diagnostics.append(
            Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=5),
                ),
                message=f"Internal Compiler Error: {str(e)}",
                severity=DiagnosticSeverity.Error,
                source="AAYU Compiler"
            )
        )

    ls.publish_diagnostics(uri, diagnostics)

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    validate_aayu_document(ls, params.text_document.uri, params.text_document.text)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LanguageServer, params: DidChangeTextDocumentParams):
    # In full implementation, we might apply incremental text edits,
    # but for prototype, we just grab the full document from workspace
    doc = ls.workspace.get_document(params.text_document.uri)
    validate_aayu_document(ls, params.text_document.uri, doc.source)

if __name__ == "__main__":
    server.start_io()
