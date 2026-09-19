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
from compiler.backend.html_generator import HTMLGenerator
# # from compiler.frontend.v2.compiler import CompilerV2

def test_html_generator():
    c = CompilerV2()
    # It just needs a valid AST or something.
    gen = HTMLGenerator(None, "output")
    assert gen.out_dir == "output"
    # Testing actual generation is complex without full AST, so we just init
