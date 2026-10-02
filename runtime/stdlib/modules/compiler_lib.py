import json, io, sys
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.session.manager import SessionManager
from ...values.string import StringValue
from ...values.map import MapValue
from ...values.list import ListValue
from ...values.number import NumberValue

def register_compiler_lib(registry):
    def fn_compile(args, vm):
        if not args:
            raise Exception("compiler::compile takes 1 argument (code)")
        code = str(args[0].value) if hasattr(args[0], 'value') else str(args[0])

        result = {
            "success": 1.0,
            "tokens": [],
            "ast": None,
            "bytecode": [],
            "vm_output": "",
            "errors": []
        }

        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            result["tokens"] = [str(t) for t in tokens]

            parser = Parser(tokens)
            ast = parser.parse()
            if ast:
                def ast_to_dict(node):
                    if isinstance(node, list):
                        return [ast_to_dict(item) for item in node]
                    if not hasattr(node, '__dict__'):
                        return str(node)
                    d = {"type": type(node).__name__}
                    for k, v in node.__dict__.items():
                        if k != 'line':
                            d[k] = ast_to_dict(v)
                    return d
                result["ast"] = ast_to_dict(ast)

                analyzer = SemanticAnalyzer(ast)
                analyzer.analyze()

                pipeline = IRPipeline(ast)
                lir = pipeline.lower()

                encoder = BytecodeEncoder(lir, analyzer.get_state())
                bc, actions, db_schema = encoder.encode()

                instr_map = {}
                import compiler.bytecode.instructions as instr
                for name, value in vars(instr.Opcode).items():
                    if isinstance(value, int) and not name.startswith('_'):
                        instr_map[value] = name

                bc_str = []
                i = 0
                while i < len(bc):
                    op = bc[i]
                    op_name = instr_map.get(op, f"UNKNOWN_{op}")
                    if op in [instr.Opcode.PUSH_CONST, instr.Opcode.LOAD_STATE, instr.Opcode.STORE_STATE,
                              instr.Opcode.JMP, instr.Opcode.JMP_IF_FALSE, instr.Opcode.CALL,
                              instr.Opcode.CALL_ACTION, instr.Opcode.CALL_COMPONENT, instr.Opcode.INIT_COMPONENT_STATE]:
                        idx = int.from_bytes(bc[i+1:i+3], 'little')
                        bc_str.append(f"{op_name} {idx}")
                        i += 3
                    else:
                        bc_str.append(op_name)
                        i += 1
                result["bytecode"] = bc_str

                session = SessionManager()
                session.init_with_bytecode(bc, actions, db_schema)
                session.start()

        except Exception as e:
            result["success"] = 0.0
            result["errors"].append(str(e))

        sys.stdout = old_stdout
        result["vm_output"] = redirected_output.getvalue()

        # Convert result dict to AAYU MapValue
        map_val = MapValue({})
        map_val.elements["success"] = NumberValue(result["success"])
        
        tokens_list = ListValue([])
        for t in result["tokens"]:
            tokens_list.elements.append(StringValue(t))
        map_val.elements["tokens"] = tokens_list
        
        bc_list = ListValue([])
        for b in result["bytecode"]:
            bc_list.elements.append(StringValue(b))
        map_val.elements["bytecode"] = bc_list
        
        err_list = ListValue([])
        for e in result["errors"]:
            err_list.elements.append(StringValue(e))
        map_val.elements["errors"] = err_list
        
        map_val.elements["vm_output"] = StringValue(result["vm_output"])
        map_val.elements["ast"] = StringValue(json.dumps(result["ast"]))
        
        return map_val

    registry.register("compiler::compile", fn_compile)
