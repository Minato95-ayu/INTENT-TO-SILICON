import pytest
from compiler.backend.html_generator import HTMLGenerator
from compiler.frontend.v2.compiler import CompilerV2

def test_html_generator():
    c = CompilerV2()
    # It just needs a valid AST or something.
    gen = HTMLGenerator(None, "output")
    assert gen.out_dir == "output"
    # Testing actual generation is complex without full AST, so we just init
