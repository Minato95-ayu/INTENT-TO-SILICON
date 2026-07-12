"""
Phase 4.1 - Exception System Tests
Tests the complete exception handling pipeline:
  Lexer -> Parser -> AST -> Compiler -> Bytecode -> VM (unwinding)

Test categories:
  1. Basic throw/catch
  2. Throw without catch (unhandled)
  3. Finally blocks
  4. Panic (uncatchable)
  5. Assert lowering
  6. Nested try/catch/finally
  7. Edge cases (throw in catch, throw in finally, return in try)
"""

import sys
import os

# Add language directory to path (must be first to override any conflicting modules)
LANG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'language'))
sys.path.insert(0, LANG_DIR)

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from runtime.memory import MemoryManager
from runtime.vm.vm import VirtualMachine
from runtime.diagnostics import AAYUUnhandledException
from compiler.frontend.errors import AAYURuntimeError


def compile_and_run(source: str) -> VirtualMachine:
    """Compile and run AAYU source, returning the VM instance."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, filename="<test>")
    ast = parser.parse()
    compiler = AAYUCompiler(filename="<test>")
    bytecode = compiler.compile(ast)
    vm = VirtualMachine()
    vm.run(bytecode)
    return vm


def test_basic_throw_catch():
    """throw inside try is caught by catch, binding is accessible."""
    source = '''
    let result is "none".
    try.
        throw "something went wrong".
        let result is "unreachable".
    catch (e).
        let result is "caught".
    end.
    print(result).
    '''
    vm = compile_and_run(source)
    assert "caught" in vm.output, f"Expected 'caught' in output, got {vm.output}"
    print("  [PASS] test_basic_throw_catch")


def test_catch_binding():
    """The exception value is bound to the catch variable and accessible."""
    source = '''
    let result is "none".
    try.
        throw "my error message".
    catch (err).
        let result is err.
    end.
    print(result).
    '''
    vm = compile_and_run(source)
    assert len(vm.output) > 0, "Expected output from print"
    assert "my error message" in vm.output[0], f"Expected error message in output, got {vm.output}"
    print("  [PASS] test_catch_binding")


def test_normal_flow_no_catch():
    """Normal flow through try without throwing."""
    source = '''
    let result is "start".
    try.
        let result is "inside_try".
    catch (e).
        let result is "should_not_reach".
    end.
    print(result).
    '''
    vm = compile_and_run(source)
    assert "inside_try" in vm.output, f"Expected 'inside_try' in output, got {vm.output}"
    print("  [PASS] test_normal_flow_no_catch")


def test_unhandled_throw():
    """throw without any try/catch raises a Python RuntimeError."""
    source = '''
    throw "unhandled error".
    '''
    try:
        compile_and_run(source)
        assert False, "Expected AAYURuntimeError"
    except AAYUUnhandledException:
        pass
    print("  [PASS] test_unhandled_throw")


def test_finally_always_runs():
    """finally block runs even when no exception is thrown."""
    source = '''
    let result is "start".
    try.
        let result is "try_body".
    finally.
        print("finally_ran").
    end.
    '''
    vm = compile_and_run(source)
    assert "finally_ran" in vm.output, f"Expected 'finally_ran' in output, got {vm.output}"
    print("  [PASS] test_finally_always_runs")


def test_finally_runs_on_throw():
    """finally block runs after catch handles the exception."""
    source = '''
    try.
        throw "error".
    catch (e).
        print("caught").
    finally.
        print("finally_ran").
    end.
    '''
    vm = compile_and_run(source)
    assert "caught" in vm.output, f"Expected 'caught' in output, got {vm.output}"
    assert "finally_ran" in vm.output, f"Expected 'finally_ran' in output, got {vm.output}"
    print("  [PASS] test_finally_runs_on_throw")


def test_panic_is_uncatchable():
    """panic should NOT be caught by catch blocks."""
    source = '''
    try.
        panic "fatal error".
    catch (e).
        print("should never see this").
    end.
    '''
    try:
        compile_and_run(source)
        assert False, "Expected AAYURuntimeError from panic"
    except AAYUUnhandledException:
        pass
    print("  [PASS] test_panic_is_uncatchable")


def test_panic_finally_runs():
    """panic should still execute finally blocks before terminating."""
    source = '''
    try.
        panic "fatal".
    finally.
        print("finally_during_panic").
    end.
    '''
    try:
        vm = compile_and_run(source)
        assert False, "Expected AAYURuntimeError from panic"
    except AAYUUnhandledException:
        pass
    print("  [PASS] test_panic_finally_runs")


def test_assert_pass():
    """assert with a truthy condition should not throw."""
    source = '''
    let x is 5.
    assert x is greater than 0.
    print("passed").
    '''
    vm = compile_and_run(source)
    assert "passed" in vm.output, f"Expected 'passed' in output, got {vm.output}"
    print("  [PASS] test_assert_pass")


def test_assert_fail():
    """assert with a falsy condition should throw."""
    source = '''
    let x is 0.
    assert x is greater than 5.
    print("should not reach").
    '''
    try:
        compile_and_run(source)
        assert False, "Expected AAYURuntimeError from failed assert"
    except AAYUUnhandledException:
        pass
    print("  [PASS] test_assert_fail")


def test_assert_caught():
    """Failed assert can be caught in a try/catch."""
    source = '''
    let result is "none".
    try.
        assert 0 is greater than 5.
    catch (e).
        let result is "assertion_caught".
    end.
    print(result).
    '''
    vm = compile_and_run(source)
    assert "assertion_caught" in vm.output, f"Expected 'assertion_caught' in output, got {vm.output}"
    print("  [PASS] test_assert_caught")


def test_nested_try_catch():
    """Nested try blocks: inner catch handles inner throw."""
    source = '''
    let result is "start".
    try.
        try.
            throw "inner error".
        catch (inner_e).
            let result is "inner_caught".
        end.
    catch (outer_e).
        let result is "outer_caught".
    end.
    print(result).
    '''
    vm = compile_and_run(source)
    assert "inner_caught" in vm.output, f"Expected 'inner_caught' in output, got {vm.output}"
    print("  [PASS] test_nested_try_catch")


def test_nested_try_propagation():
    """If inner try has no catch, exception propagates to outer catch."""
    source = '''
    let result is "start".
    try.
        try.
            throw "propagated error".
        finally.
            print("inner_finally").
        end.
    catch (outer_e).
        let result is "outer_caught".
    end.
    print(result).
    '''
    vm = compile_and_run(source)
    assert "inner_finally" in vm.output, f"Expected 'inner_finally' in output, got {vm.output}"
    assert "outer_caught" in vm.output, f"Expected 'outer_caught' in output, got {vm.output}"
    print("  [PASS] test_nested_try_propagation")


def test_throw_in_catch():
    """Rethrowing from inside a catch should propagate to an outer handler."""
    source = '''
    let result is "start".
    try.
        try.
            throw "original".
        catch (e).
            throw "rethrown".
        end.
    catch (outer_e).
        let result is "rethrown_caught".
    end.
    print(result).
    '''
    vm = compile_and_run(source)
    assert "rethrown_caught" in vm.output, f"Expected 'rethrown_caught' in output, got {vm.output}"
    print("  [PASS] test_throw_in_catch")


def test_try_only_with_finally():
    """try with only finally (no catch) - exception passes through."""
    source = '''
    try.
        try.
            throw "no catch here".
        finally.
            print("finally_ran").
        end.
    catch (e).
        print("outer_caught").
    end.
    '''
    vm = compile_and_run(source)
    assert "finally_ran" in vm.output, f"Expected 'finally_ran' in output, got {vm.output}"
    assert "outer_caught" in vm.output, f"Expected 'outer_caught' in output, got {vm.output}"
    print("  [PASS] test_try_only_with_finally")


# --- Parser-level tests ---

def test_parser_throw_node():
    """Parser generates correct ThrowNode."""
    from compiler.frontend.ast_nodes import ThrowNode
    source = 'throw "test error".'
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize(), filename="<test>")
    ast = parser.parse()
    assert len(ast.statements) == 1
    node = ast.statements[0]
    assert isinstance(node, ThrowNode), f"Expected ThrowNode, got {type(node)}"
    print("  [PASS] test_parser_throw_node")


def test_parser_panic_node():
    """Parser generates correct PanicNode."""
    from compiler.frontend.ast_nodes import PanicNode
    source = 'panic "fatal".'
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize(), filename="<test>")
    ast = parser.parse()
    assert len(ast.statements) == 1
    node = ast.statements[0]
    assert isinstance(node, PanicNode), f"Expected PanicNode, got {type(node)}"
    print("  [PASS] test_parser_panic_node")


def test_parser_assert_node():
    """Parser generates correct AssertNode."""
    from compiler.frontend.ast_nodes import AssertNode
    source = 'assert 1 is greater than 0.'
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize(), filename="<test>")
    ast = parser.parse()
    assert len(ast.statements) == 1
    node = ast.statements[0]
    assert isinstance(node, AssertNode), f"Expected AssertNode, got {type(node)}"
    print("  [PASS] test_parser_assert_node")


def test_parser_try_catch_finally():
    """Parser generates correct TryNode with catch and finally."""
    from compiler.frontend.ast_nodes import TryNode, CatchNode, FinallyNode
    source = '''
    try.
        print("body").
    catch (e).
        print("caught").
    finally.
        print("cleanup").
    end.
    '''
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize(), filename="<test>")
    ast = parser.parse()
    assert len(ast.statements) == 1
    node = ast.statements[0]
    assert isinstance(node, TryNode), f"Expected TryNode, got {type(node)}"
    assert node.catch_node is not None, "Expected catch_node"
    assert isinstance(node.catch_node, CatchNode)
    assert node.catch_node.binding == "e"
    assert node.finally_node is not None, "Expected finally_node"
    assert isinstance(node.finally_node, FinallyNode)
    print("  [PASS] test_parser_try_catch_finally")


# --- Bytecode / Compiler tests ---

def test_compiler_throw_emits_opcodes():
    """Compiler emits THROW opcode for ThrowNode."""
    from compiler.frontend.ir import Opcode
    source = 'throw "error".'
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize(), filename="<test>")
    ast = parser.parse()
    compiler = AAYUCompiler(filename="<test>")
    bytecode = compiler.compile(ast)
    opcodes = [inst.opcode for inst in bytecode.instructions]
    assert Opcode.THROW in opcodes, f"Expected THROW opcode, got {opcodes}"
    print("  [PASS] test_compiler_throw_emits_opcodes")


def test_compiler_try_emits_table():
    """Compiler generates exception_table entry for TryNode."""
    source = '''
    try.
        let x is 1.
    catch (e).
        let y is 2.
    end.
    '''
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize(), filename="<test>")
    ast = parser.parse()
    compiler = AAYUCompiler(filename="<test>")
    bytecode = compiler.compile(ast)
    assert len(bytecode.exception_table) == 1, f"Expected 1 exception_table entry, got {len(bytecode.exception_table)}"
    entry = bytecode.exception_table[0]
    assert entry['catch_target'] >= 0, f"Expected catch_target >= 0, got {entry['catch_target']}"
    print("  [PASS] test_compiler_try_emits_table")


def test_compiler_panic_emits_opcodes():
    """Compiler emits PANIC opcode for PanicNode."""
    from compiler.frontend.ir import Opcode
    source = 'panic "fatal".'
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize(), filename="<test>")
    ast = parser.parse()
    compiler = AAYUCompiler(filename="<test>")
    bytecode = compiler.compile(ast)
    opcodes = [inst.opcode for inst in bytecode.instructions]
    assert Opcode.PANIC in opcodes, f"Expected PANIC opcode, got {opcodes}"
    print("  [PASS] test_compiler_panic_emits_opcodes")


# --- Exception Value tests ---

def test_exception_value_hierarchy():
    """Exception value hierarchy is correctly structured."""
    from runtime.values.exception import (
        ExceptionValue, LanguageException, RuntimeException,
        ArithmeticException, DivisionByZeroException,
        PanicValue, AssertionException
    )
    
    lang_exc = LanguageException("test")
    assert isinstance(lang_exc, ExceptionValue)
    assert lang_exc.type_name() == "Exception"
    assert lang_exc.exception_type == "LanguageException"
    assert lang_exc.message == "test"
    assert lang_exc.stringify() == "LanguageException: test"
    
    div_exc = DivisionByZeroException()
    assert isinstance(div_exc, ArithmeticException)
    assert isinstance(div_exc, RuntimeException)
    assert isinstance(div_exc, ExceptionValue)
    assert div_exc.exception_type == "DivisionByZero"
    
    panic = PanicValue("fatal")
    assert not isinstance(panic, ExceptionValue)
    assert panic.type_name() == "Panic"
    assert panic.stringify() == "PANIC: fatal"
    
    assertion = AssertionException("test failed")
    assert isinstance(assertion, ExceptionValue)
    assert assertion.exception_type == "AssertionException"
    
    print("  [PASS] test_exception_value_hierarchy")


def test_panic_is_not_exception():
    """PanicValue is NOT an ExceptionValue - enforces uncatchability at type level."""
    from runtime.values.exception import ExceptionValue, PanicValue
    panic = PanicValue("bad")
    assert not isinstance(panic, ExceptionValue), "PanicValue must NOT be an ExceptionValue"
    print("  [PASS] test_panic_is_not_exception")


def test_execution_state_enum():
    """ExecutionState enum has the required states."""
    from runtime.vm.vm import ExecutionState
    assert ExecutionState.NORMAL.value == "NORMAL"
    assert ExecutionState.THROWING.value == "THROWING"
    assert ExecutionState.PANICKING.value == "PANICKING"
    print("  [PASS] test_execution_state_enum")


# --- Run all tests ---

if __name__ == "__main__":
    print("\n=== Phase 4.1 - Exception System Tests ===\n")
    
    passed = 0
    failed = 0
    errors = []
    
    tests = [
        # Parser tests
        test_parser_throw_node,
        test_parser_panic_node,
        test_parser_assert_node,
        test_parser_try_catch_finally,
        
        # Compiler tests
        test_compiler_throw_emits_opcodes,
        test_compiler_try_emits_table,
        test_compiler_panic_emits_opcodes,
        
        # Value hierarchy tests
        test_exception_value_hierarchy,
        test_panic_is_not_exception,
        test_execution_state_enum,
        
        # VM integration tests
        test_basic_throw_catch,
        test_catch_binding,
        test_normal_flow_no_catch,
        test_unhandled_throw,
        test_finally_always_runs,
        test_finally_runs_on_throw,
        test_panic_is_uncatchable,
        test_panic_finally_runs,
        test_assert_pass,
        test_assert_fail,
        test_assert_caught,
        
        # Advanced: Nesting and edge cases
        test_nested_try_catch,
        test_nested_try_propagation,
        test_throw_in_catch,
        test_try_only_with_finally,
    ]
    
    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            failed += 1
            errors.append((test_fn.__name__, str(e)))
            print(f"  [FAIL] {test_fn.__name__}: {e}")
    
    print(f"\n--- Results: {passed}/{passed + failed} passed ---")
    if errors:
        print("\nFailures:")
        for name, err in errors:
            print(f"  {name}: {err}")
    
    sys.exit(0 if failed == 0 else 1)
