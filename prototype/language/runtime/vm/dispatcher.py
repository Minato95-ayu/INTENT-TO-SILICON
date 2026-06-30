from ir import Opcode
from .instructions import *

DISPATCH_TABLE = {
    Opcode.LOAD_CONST: execute_load_const,
    Opcode.LOAD_VAR: execute_load_var,
    Opcode.STORE_VAR: execute_store_var,
    Opcode.ADD: execute_add,
    Opcode.SUB: execute_sub,
    Opcode.MUL: execute_mul,
    Opcode.DIV: execute_div,
    Opcode.EQ: execute_eq,
    Opcode.LT: execute_lt,
    Opcode.GT: execute_gt,
    Opcode.JUMP: execute_jump,
    Opcode.JUMP_IF_FALSE: execute_jump_if_false,
    Opcode.CALL: execute_call,
    Opcode.RETURN: execute_return,
}
