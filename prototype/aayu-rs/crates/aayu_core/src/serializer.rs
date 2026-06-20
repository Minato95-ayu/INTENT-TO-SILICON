use crate::bytecode::Bytecode;
use std::error::Error;

pub fn deserialize_from_str(json_str: &str) -> Result<Bytecode, Box<dyn Error>> {
    let bytecode: Bytecode = serde_json::from_str(json_str)?;
    Ok(bytecode)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::opcode::Opcode;

    #[test]
    fn test_deserialization() {
        let json_data = r#"{
            "name": "main",
            "file": "test.aayu",
            "constants": ["hello", 42.0, true],
            "names": ["x"],
            "parameters": [],
            "instructions": [
                {"opcode": 1, "operand": 0, "line": 1, "file": "test.aayu"},
                {"opcode": 3, "operand": 0, "line": 2, "file": "test.aayu"},
                {"opcode": 23, "line": 3, "file": "test.aayu"}
            ],
            "tasks": {}
        }"#;

        let bc = deserialize_from_str(json_data).unwrap();
        assert_eq!(bc.name, "main");
        assert_eq!(bc.constants.len(), 3);
        assert_eq!(bc.instructions[0].opcode, Opcode::LoadConst);
        assert_eq!(bc.instructions[2].opcode, Opcode::Return);
    }
}
