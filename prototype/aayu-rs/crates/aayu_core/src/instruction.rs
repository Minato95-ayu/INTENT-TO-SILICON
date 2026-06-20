use crate::opcode::Opcode;
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub struct Instruction {
    pub opcode: Opcode,
    pub operand: Option<usize>,
    pub line: Option<usize>,
    pub file: Option<String>,
}

impl Serialize for Instruction {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        use serde::ser::SerializeSeq;
        let mut seq = serializer.serialize_seq(Some(4))?;
        seq.serialize_element(&self.opcode)?;
        seq.serialize_element(&self.operand)?;
        seq.serialize_element(&self.line)?;
        seq.serialize_element(&self.file)?;
        seq.end()
    }
}

impl<'de> Deserialize<'de> for Instruction {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct InstructionVisitor;

        impl<'de> serde::de::Visitor<'de> for InstructionVisitor {
            type Value = Instruction;

            fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
                formatter.write_str("an Instruction map or array sequence")
            }

            // Handle object format: {"opcode": ..., "operand": ..., "line": ..., "file": ...}
            fn visit_map<A>(self, mut map: A) -> Result<Self::Value, A::Error>
            where
                A: serde::de::MapAccess<'de>,
            {
                let mut opcode = None;
                let mut operand = None;
                let mut line = None;
                let mut file = None;

                while let Some(key) = map.next_key::<String>()? {
                    match key.as_str() {
                        "opcode" => {
                            opcode = Some(map.next_value()?);
                        }
                        "operand" => {
                            operand = map.next_value()?;
                        }
                        "line" => {
                            line = map.next_value()?;
                        }
                        "file" => {
                            file = map.next_value()?;
                        }
                        _ => {
                            let _: serde::de::IgnoredAny = map.next_value()?;
                        }
                    }
                }

                let opcode = opcode.ok_or_else(|| serde::de::Error::missing_field("opcode"))?;
                Ok(Instruction {
                    opcode,
                    operand,
                    line,
                    file,
                })
            }

            // Handle array sequence format: [opcode, operand, line, file] or shorter
            fn visit_seq<A>(self, mut seq: A) -> Result<Self::Value, A::Error>
            where
                A: serde::de::SeqAccess<'de>,
            {
                let opcode: Opcode = seq.next_element()?
                    .ok_or_else(|| serde::de::Error::invalid_length(0, &"at least 1 element for opcode"))?;
                
                let operand: Option<usize> = seq.next_element()?.flatten();
                let line: Option<usize> = seq.next_element()?.flatten();
                let file: Option<String> = seq.next_element()?.flatten();

                Ok(Instruction {
                    opcode,
                    operand,
                    line,
                    file,
                })
            }
        }

        deserializer.deserialize_any(InstructionVisitor)
    }
}
