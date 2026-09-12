import pytest
import os
import tempfile
from tools.aayu_lsp import run_lsp
from tools.lsp_server import LanguageServer

def test_lsp_server():
    server = LanguageServer()
    assert server is not None
    
    # Check diagnostics
    diagnostics = server.get_diagnostics("function test() return 1. end.")
    assert isinstance(diagnostics, list)
