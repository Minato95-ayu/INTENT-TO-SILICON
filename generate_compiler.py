
# AAYU Self-Hosted Compiler (AST to Bytecode)

let OP_PUSH_CONST = 1
let OP_POP = 2
let OP_ADD = 16
let OP_SUB = 17
let OP_MUL = 18
let OP_DIV = 19
let OP_JMP = 32
let OP_JMP_IF_FALSE = 33
let OP_CALL = 34
let OP_RET = 35
let OP_CMP_EQ = 38
let OP_CMP_NEQ = 39
let OP_CMP_LT = 41
let OP_CMP_GT = 42
let OP_CMP_LTE = 43
let OP_CMP_GTE = 44
let OP_STORE_STATE = 48
let OP_LOAD_STATE = 49
let OP_PRINT = 81
let OP_RETURN_VALUE = 98
let OP_CREATE_ARRAY = 134
let OP_BUILD_DICT = 128
let OP_LOAD_SUBSCR = 136
let OP_STORE_SUBSCR = 137

# Globals
let constants = []
let bytecode = []

action add_constant(value)
    let ac_idx = 0
    let ac_len = len(constants)
    let ac_found = 1 == 0
    
    while ac_idx < ac_len
        if constants[ac_idx] == value
            ac_found = 1 == 1
            return ac_idx
        end
        ac_idx = ac_idx + 1
    end
    
    constants = constants + [value]
    return ac_len
end

action emit(opcode, arg1, arg2)
    bytecode = bytecode + [opcode, arg1, arg2]
    return 0
end

action emit_patchable(opcode)
    let ep_idx = len(bytecode)
    bytecode = bytecode + [opcode, 255, 255]
    return ep_idx
end

action patch_jump(ep_idx)
    let pj_target = len(bytecode)
    bytecode[ep_idx + 1] = pj_target
    return 0
end

action compile_expression(expr)
    let ce_type = expr["type"]
    let ce_idx = 0
    let ce_op = ""
    let ce_i = 0
    let ce_len = 0
    let ce_args = []
    
    if ce_type == "Number"
        ce_idx = add_constant(expr["value"])
        emit(OP_PUSH_CONST, ce_idx, 0)
    end
    if ce_type == "String"
        ce_idx = add_constant(expr["value"])
        emit(OP_PUSH_CONST, ce_idx, 0)
    end
    if ce_type == "Literal"
        ce_idx = add_constant(expr["value"])
        emit(OP_PUSH_CONST, ce_idx, 0)
    end
    if ce_type == "Identifier"
        ce_idx = add_constant(expr["name"])
        emit(OP_LOAD_STATE, ce_idx, 0)
    end
    if ce_type == "Array"
        ce_args = expr["elements"]
        ce_i = 0
        ce_len = len(ce_args)
        while ce_i < ce_len
            compile_expression(ce_args[ce_i])
            ce_i = ce_i + 1
        end
        emit(OP_CREATE_ARRAY, ce_len, 0)
    end
    if ce_type == "Dictionary"
        ce_args = expr["keys"]
        let ce_vals = expr["values"]
        ce_i = 0
        ce_len = len(ce_args)
        while ce_i < ce_len
            compile_expression(ce_vals[ce_i])
            compile_expression(ce_args[ce_i])
            ce_i = ce_i + 1
        end
        emit(OP_BUILD_DICT, ce_len, 0)
    end
    if ce_type == "Subscript"
        compile_expression(expr["target"])
        compile_expression(expr["index"])
        emit(OP_LOAD_SUBSCR, 0, 0)
    end
    if ce_type == "ActionCall"
        ce_idx = add_constant(expr["name"])
        emit(OP_PUSH_CONST, ce_idx, 0)
        ce_args = expr["args"]
        ce_i = 0
        ce_len = len(ce_args)
        while ce_i < ce_len
            compile_expression(ce_args[ce_i])
            ce_i = ce_i + 1
        end
        emit(OP_CALL, ce_len, 0)
    end
    if ce_type == "BinaryOp"
        compile_expression(expr["left"])
        compile_expression(expr["right"])
        ce_op = expr["operator"]
        if ce_op == "+"
            emit(OP_ADD, 0, 0)
        end
        if ce_op == "-"
            emit(OP_SUB, 0, 0)
        end
        if ce_op == "*"
            emit(OP_MUL, 0, 0)
        end
        if ce_op == "/"
            emit(OP_DIV, 0, 0)
        end
        if ce_op == "=="
            emit(OP_CMP_EQ, 0, 0)
        end
        if ce_op == "!="
            emit(OP_CMP_NEQ, 0, 0)
        end
        if ce_op == "<"
            emit(OP_CMP_LT, 0, 0)
        end
        if ce_op == ">"
            emit(OP_CMP_GT, 0, 0)
        end
        if ce_op == "<="
            emit(OP_CMP_LTE, 0, 0)
        end
        if ce_op == ">="
            emit(OP_CMP_GTE, 0, 0)
        end
    end
    return 0
end

action compile_statement(stmt)
    let cs_type = stmt["type"]
    let cs_idx = 0
    let cs_body = []
    let cs_else = []
    let cs_i = 0
    let cs_len = 0
    let cs_jmp1 = 0
    let cs_jmp2 = 0
    
    if cs_type == "LetDeclaration"
        compile_expression(stmt["value"])
        cs_idx = add_constant(stmt["name"])
        emit(OP_STORE_STATE, cs_idx, 0)
    end
    if cs_type == "Assignment"
        let cs_target = stmt["target"]
        if cs_target["type"] == "Identifier"
            compile_expression(stmt["value"])
            cs_idx = add_constant(cs_target["name"])
            emit(OP_STORE_STATE, cs_idx, 0)
        end
        if cs_target["type"] == "Subscript"
            compile_expression(cs_target["target"])
            compile_expression(cs_target["index"])
            compile_expression(stmt["value"])
            emit(OP_STORE_SUBSCR, 0, 0)
        end
    end
    if cs_type == "If"
        compile_expression(stmt["condition"])
        cs_jmp1 = emit_patchable(OP_JMP_IF_FALSE)
        
        cs_body = stmt["then_branch"]
        cs_i = 0
        cs_len = len(cs_body)
        while cs_i < cs_len
            compile_statement(cs_body[cs_i])
            cs_i = cs_i + 1
        end
        
        cs_else = stmt["else_branch"]
        if len(cs_else) > 0
            cs_jmp2 = emit_patchable(OP_JMP)
            patch_jump(cs_jmp1)
            
            cs_i = 0
            cs_len = len(cs_else)
            while cs_i < cs_len
                compile_statement(cs_else[cs_i])
                cs_i = cs_i + 1
            end
            patch_jump(cs_jmp2)
        else
            patch_jump(cs_jmp1)
        end
    end
    if cs_type == "While"
        let cs_while_start = len(bytecode)
        compile_expression(stmt["condition"])
        cs_jmp1 = emit_patchable(OP_JMP_IF_FALSE)
        
        cs_body = stmt["body"]
        cs_i = 0
        cs_len = len(cs_body)
        while cs_i < cs_len
            compile_statement(cs_body[cs_i])
            cs_i = cs_i + 1
        end
        
        emit(OP_JMP, cs_while_start, 0)
        patch_jump(cs_jmp1)
    end
    if cs_type == "Return"
        if stmt["value"] != ""
            compile_expression(stmt["value"])
        else
            cs_idx = add_constant("")
            emit(OP_PUSH_CONST, cs_idx, 0)
        end
        emit(OP_RETURN_VALUE, 0, 0)
    end
    if cs_type == "ActionDeclaration"
        cs_jmp1 = emit_patchable(OP_JMP)
        
        cs_body = stmt["statements"]
        cs_i = 0
        cs_len = len(cs_body)
        while cs_i < cs_len
            compile_statement(cs_body[cs_i])
            cs_i = cs_i + 1
        end
        
        patch_jump(cs_jmp1)
    end
    if cs_type == "ExpressionStatement"
        compile_expression(stmt["expression"])
        emit(OP_POP, 0, 0)
    end
    return 0
end

action compile(ast)
    if ast["type"] == "Program"
        let cp_stmts = ast["statements"]
        let cp_i = 0
        let cp_len = len(cp_stmts)
        while cp_i < cp_len
            compile_statement(cp_stmts[cp_i])
            cp_i = cp_i + 1
        end
    end
    return 0
end

# A more complex AST from phase 2!
let sample_ast = { 
    "type": "Program", 
    "statements": [
        { 
            "type": "ActionDeclaration", 
            "name": "factorial", 
            "args": ["n"], 
            "statements": [
                {
                    "type": "If",
                    "condition": {
                        "type": "BinaryOp",
                        "operator": "<=",
                        "left": { "type": "Identifier", "name": "n" },
                        "right": { "type": "Number", "value": 1 }
                    },
                    "then_branch": [
                        {
                            "type": "Return",
                            "value": { "type": "Number", "value": 1 }
                        }
                    ],
                    "else_branch": [
                        {
                            "type": "Return",
                            "value": {
                                "type": "BinaryOp",
                                "operator": "*",
                                "left": { "type": "Identifier", "name": "n" },
                                "right": {
                                    "type": "ActionCall",
                                    "name": "factorial",
                                    "args": [
                                        {
                                            "type": "BinaryOp",
                                            "operator": "-",
                                            "left": { "type": "Identifier", "name": "n" },
                                            "right": { "type": "Number", "value": 1 }
                                        }
                                    ]
                                }
                            }
                        }
                    ]
                }
            ] 
        }
    ] 
}

compile(sample_ast)

print("Compiler Success: Complex Program Compiled!")
print("Constants Pool:")
print(constants)
print("Bytecode Array Length: ")
print(len(bytecode))
print("Bytecode Array: ")
print(bytecode)
