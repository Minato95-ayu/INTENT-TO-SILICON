import sys, os
sys.path.insert(0, '.')

print("=" * 50)
print("  AAYU FRAMEWORK STATUS CHECK")
print("=" * 50)

# --- 1. Compiler Pipeline ---
print("\n[1] COMPILER PIPELINE")
try:
    from aayu.compiler.lexer.lexer import Lexer
    from aayu.compiler.parser.parser import Parser
    from aayu.compiler.semantic.analyzer import SemanticAnalyzer
    from aayu.compiler.ir.pipeline import IRPipeline
    from aayu.compiler.bytecode.encoder import BytecodeEncoder
    from aayu.compiler.bytecode.disassembler import disassemble_with_header

    src = '''
Form Login
    validate
        email: required email
        password: minLength 8
    end

    Input
        bind email
    end

    Button "Submit"
        onClick Submit
    end
end
'''
    t = Lexer(src).tokenize()
    a = Parser(t).parse()
    s = SemanticAnalyzer().analyze(a)
    p = IRPipeline()
    prog = BytecodeEncoder().encode(p.to_lir(p.to_mir(p.to_hir(s))))
    print("  Lexer:       OK")
    print("  Parser:      OK")
    print("  Semantic:    OK")
    print("  IR Pipeline: OK")
    print("  Encoder:     OK")
    print(f"  Bytecode:    {len(prog.bytecode)} bytes, {len(prog.constant_pool)} constants")
except Exception as e:
    print(f"  FAILED: {e}")

# --- 2. FormState Engine ---
print("\n[2] FORMSTATE ENGINE")
try:
    from aayu.runtime.vm.form_state import FormStateManager

    class MockVM:
        state_scopes = [{"__instance_id__": "test"}]

    fsm = FormStateManager(MockVM())
    fsm.init_form()
    form = fsm.get_form()
    assert form is not None, "Form not initialized"
    assert form["valid"] == True, "Form should be valid by default"

    fsm.set_rules("$form", {
        "email": [{"rule": "required", "args": []}, {"rule": "email", "args": []}],
        "password": [{"rule": "minLength", "args": [8]}]
    })

    # Test: empty email should fail
    r1 = fsm.validate_field("$form", "email", "")
    assert r1 == False, "Empty email should be invalid"

    # Test: valid email should pass
    r2 = fsm.validate_field("$form", "email", "test@example.com")
    assert r2 == True, "Valid email should be valid"

    # Test: short password should fail
    r3 = fsm.validate_field("$form", "password", "abc")
    assert r3 == False, "Short password should be invalid"

    # Test: valid password should pass
    r4 = fsm.validate_field("$form", "password", "longpassword123")
    assert r4 == True, "Valid password should be valid"

    # Test update_field triggers validation
    fsm.update_field("$form", "email", "bad")
    form = fsm.get_form()
    assert form["valid"] == False, "Form with bad email should be invalid"
    assert "email" in form["errors"], "Should have email error"

    fsm.update_field("$form", "email", "good@email.com")
    form = fsm.get_form()
    assert form["valid"] == True, "Form with good email should be valid"
    assert "email" not in form["errors"], "Should not have email error"

    print("  init_form:        OK")
    print("  set_rules:        OK")
    print("  validate (req):   OK")
    print("  validate (email): OK")
    print("  validate (minL):  OK")
    print("  update_field:     OK")
    print("  error tracking:   OK")
    print("  validity recalc:  OK")
except Exception as e:
    print(f"  FAILED: {e}")
    import traceback; traceback.print_exc()

# --- 3. VM Infrastructure ---
print("\n[3] VM INFRASTRUCTURE")
try:
    from aayu.runtime.vm.vm import VirtualMachine
    from aayu.runtime.vm.instructions import Opcode
    vm = VirtualMachine.__new__(VirtualMachine)
    opcodes_defined = [name for name in dir(Opcode) if not name.startswith("_")]
    print(f"  VirtualMachine:   OK")
    print(f"  Opcodes defined:  {len(opcodes_defined)}")

    important = ["DECLARE_VALIDATION", "SET_BINDING", "DECLARE_LIFECYCLE",
                  "CALL_COMPONENT", "BUILD_WIDGET", "OP_ASYNC_CALL"]
    for op in important:
        if hasattr(Opcode, op):
            print(f"    {op}: 0x{getattr(Opcode, op):02X}")
        else:
            print(f"    {op}: MISSING!")
except Exception as e:
    print(f"  FAILED: {e}")

# --- 4. Web Renderer ---
print("\n[4] WEB RENDERER")
try:
    from aayu.runtime.renderers.web_renderer import WebRenderer
    print("  WebRenderer:      OK (importable)")
except Exception as e:
    print(f"  WebRenderer:      {e}")

# --- 5. Theme Engine ---
print("\n[5] THEME ENGINE")
try:
    from aayu.runtime.ui.theme import ThemeManager
    tm = ThemeManager.instance()
    print("  ThemeManager:     OK")
except Exception as e:
    print(f"  ThemeManager:     {e}")

# --- 6. HTTP Client ---
print("\n[6] HTTP CLIENT")
try:
    from aayu.runtime.stdlib.registry import StdLibRegistry
    reg = StdLibRegistry()
    http_funcs = [k for k in reg.functions if "http" in k.lower() or "fetch" in k.lower()]
    print(f"  StdLib functions: {len(reg.functions)}")
    print(f"  HTTP-related:     {http_funcs if http_funcs else 'None found'}")
except Exception as e:
    print(f"  FAILED: {e}")

# --- 7. Router ---
print("\n[7] ROUTER")
try:
    from aayu.runtime.vm.router import Router
    print("  Router:           OK")
except Exception as e:
    print(f"  Router:           {e}")

# --- 8. Database ---
print("\n[8] DATABASE ENGINE")
try:
    from aayu.runtime.vm.database import DatabaseEngine
    print("  DatabaseEngine:   OK")
except Exception as e:
    print(f"  DatabaseEngine:   {e}")

print("\n" + "=" * 50)
print("  STATUS CHECK COMPLETE")
print("=" * 50)
