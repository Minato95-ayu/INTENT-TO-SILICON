import sys, os
sys.path.insert(0, os.path.abspath('.'))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine

source = '''
action onLoad()
    print("Form loaded")
end

Form Login
    lifecycle
        onLoad onLoad
    end

    validate
        email: required email
        password: minLength 8
    end

    Input
        bind email
    end

    Input
        bind password
    end

    Button "Login"
        onClick Submit
    end
end

action main()
    Login()
end
'''
tokens = Lexer(source).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
prog = BytecodeEncoder().encode(pipe.to_lir(pipe.to_mir(pipe.to_hir(sem))))

vm = VirtualMachine()
vm.load(prog.bytecode, prog.constant_pool, prog.action_addresses)

print("--- Running main ---")
vm.call_action_by_name("main")

print("--- After onLoad ---")
form = vm.form_state.get_form("$form")
print("Form values:", form["values"])
print("Form errors:", form["errors"])
print("Form valid:", form["valid"])

print("--- Simulating WebRenderer Input for password ---")
vm.form_state.update_field("$form", "password", "short")
print("Form values:", form["values"])
print("Form errors:", form["errors"])
print("Form valid:", form["valid"])

print("--- Simulating valid password ---")
vm.form_state.update_field("$form", "password", "longpassword123")
print("Form values:", form["values"])
print("Form errors:", form["errors"])
print("Form valid:", form["valid"])
