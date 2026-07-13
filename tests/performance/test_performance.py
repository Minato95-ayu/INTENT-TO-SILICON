import time
import pytest
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler

def generate_large_script(loc=1000):
    lines = []
    lines.append("task main {")
    for i in range(loc):
        lines.append(f"    let var_{i} = {i} * 2.")
    lines.append("    show \"Done\".")
    lines.append("}")
    return "\n".join(lines)

def test_compilation_performance():
    source = generate_large_script(1000)
    
    start_time = time.perf_counter()
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    lex_time = time.perf_counter()
    
    parser = Parser(tokens)
    ast = parser.parse()
    parse_time = time.perf_counter()
    
    compiler = AAYUCompiler()
    bytecode = compiler.compile(ast)
    comp_time = time.perf_counter()
    
    end_time = comp_time
    duration_ms = (end_time - start_time) * 1000
    
    print(f"\nLexing: {(lex_time - start_time)*1000:.2f} ms")
    print(f"Parsing: {(parse_time - lex_time)*1000:.2f} ms")
    print(f"Compiling: {(comp_time - parse_time)*1000:.2f} ms")
    print(f"Total Compilation of 1000 LOC took: {duration_ms:.2f} ms")
    
    # CTO requirement: 1000 lines < 200ms
    assert duration_ms < 200, f"Compilation is too slow: {duration_ms:.2f} ms (Target < 200ms)"
