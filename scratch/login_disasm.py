import sys, os
sys.path.insert(0, os.path.abspath('.'))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.compiler.bytecode.disassembler import disassemble_with_header

source = """
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
"""
tokens = Lexer(source).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
prog = BytecodeEncoder().encode(pipe.to_lir(pipe.to_mir(pipe.to_hir(sem))))
print(disassemble_with_header(prog.bytecode, list(prog.constant_pool.values()), prog.header))
print(prog.action_addresses)
