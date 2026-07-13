import pytest
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from compiler.frontend.ast_nodes import *

def parse(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

def compile_source(source):
    ast = parse(source)
    compiler = AAYUCompiler()
    return compiler.compile(ast)

class TestCompilerSecurity:
    def test_compile_security_workflow(self):
        compiler = AAYUCompiler()
        ast = ProgramNode(statements=[
            RoleDefNode(name="Admin"),
            AllowDefNode(role="Admin", action="read", target_entity="User"),
            RelationDefNode(entity1="User", rel_type="one_to_many", entity2="Post"),
            CrudNode(entity_name="User"),
            WorkflowDefNode(name="RegisterUser", entity_name="User", steps=[StepDefNode(name="validate"), StepDefNode(name="save")]),
            CreateAccountNode(data_map_name="my_map"),
            LoginNode(user_map_name="my_creds"),
            LogoutNode(req_name="my_req"),
            GuardSessionNode(),
            ExportNode(declaration=VariableNode("x")),
            TryNode(try_block=[BuiltinFunctionNode(name="print", arguments=[TextNode("trying")])], catch_node=CatchNode(binding="e", block=[BuiltinFunctionNode(name="print", arguments=[TextNode("err")])]), finally_node=FinallyNode(block=[])),
            ThrowNode(expression=TextNode("err")),
            PanicNode(message=TextNode("err")),
            AssertNode(condition=TextNode("err")),
            JsonSerializeNode(data=TextNode("data")),
            UIServeNode(),
            ServeNode(port=NumberNode(3000)),
            ThemeNode(name="default", properties=[{"name": "primary", "value": TextNode("#000")}]),
            ProjectDefNode(name="MyProj"),
            UIPageNode(name="Home", elements=[]),
            RouteNode(method="GET", path=TextNode("/"), handler_name="my_handler")
        ])
        bytecode = compiler.compile(ast)
        assert bytecode
