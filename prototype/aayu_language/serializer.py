import json
from typing import Any, Dict
from ir import Bytecode, Instruction, Opcode

def bytecode_to_dict(bytecode: Bytecode) -> Dict[str, Any]:
    insts = []
    for inst in bytecode.instructions:
        insts.append([inst.opcode.name, inst.operand])
        
    consts = []
    for const in bytecode.constants:
        if isinstance(const, Bytecode):
            consts.append({"__type__": "Bytecode", "value": bytecode_to_dict(const)})
        else:
            consts.append(const)
            
    return {
        "name": bytecode.name,
        "parameters": bytecode.parameters,
        "names": bytecode.names,
        "constants": consts,
        "instructions": insts
    }

def dict_to_bytecode(d: Dict[str, Any]) -> Bytecode:
    bc = Bytecode()
    bc.name = d.get("name", "")
    bc.parameters = d.get("parameters", [])
    bc.names = d.get("names", [])
    
    for const in d.get("constants", []):
        if isinstance(const, dict) and const.get("__type__") == "Bytecode":
            bc.constants.append(dict_to_bytecode(const["value"]))
        else:
            bc.constants.append(const)
            
    for opcode_name, operand in d.get("instructions", []):
        opcode = Opcode[opcode_name]
        bc.instructions.append(Instruction(opcode, operand))
        
    return bc

def serialize(bytecode: Bytecode) -> str:
    d = bytecode_to_dict(bytecode)
    return json.dumps(d, indent=2)

def deserialize(json_str: str) -> Bytecode:
    d = json.loads(json_str)
    return dict_to_bytecode(d)
