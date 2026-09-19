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
