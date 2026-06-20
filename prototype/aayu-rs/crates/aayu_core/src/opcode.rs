use serde::{Deserialize, Deserializer, Serialize, Serializer};
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
#[repr(u8)]
pub enum Opcode {
    LoadConst = 1,
    LoadName = 2,
    StoreName = 3,
    Pop = 4,
    Add = 5,
    Sub = 6,
    Mul = 7,
    Div = 8,
    Equal = 9,
    Greater = 10,
    Less = 11,
    Not = 12,
    JumpForward = 13,
    JumpIfFalse = 14,
    JumpBackward = 15,
    Print = 16,
    BuildList = 17,
    BuildMap = 18,
    AddToList = 19,
    MapSet = 20,
    GetItem = 21,
    CallTask = 22,
    Return = 23,
}

impl Opcode {
    pub fn as_str(&self) -> &'static str {
        match self {
            Opcode::LoadConst => "LOAD_CONST",
            Opcode::LoadName => "LOAD_NAME",
            Opcode::StoreName => "STORE_NAME",
            Opcode::Pop => "POP",
            Opcode::Add => "ADD",
            Opcode::Sub => "SUB",
            Opcode::Mul => "MUL",
            Opcode::Div => "DIV",
            Opcode::Equal => "EQUAL",
            Opcode::Greater => "GREATER",
            Opcode::Less => "LESS",
            Opcode::Not => "NOT",
            Opcode::JumpForward => "JUMP_FORWARD",
            Opcode::JumpIfFalse => "JUMP_IF_FALSE",
            Opcode::JumpBackward => "JUMP_BACKWARD",
            Opcode::Print => "PRINT",
            Opcode::BuildList => "BUILD_LIST",
            Opcode::BuildMap => "BUILD_MAP",
            Opcode::AddToList => "ADD_TO_LIST",
            Opcode::MapSet => "MAP_SET",
            Opcode::GetItem => "GET_ITEM",
            Opcode::CallTask => "CALL_TASK",
            Opcode::Return => "RETURN",
        }
    }

    pub fn from_str(s: &str) -> Option<Self> {
        match s.to_uppercase().as_str() {
            "LOAD_CONST" => Some(Opcode::LoadConst),
            "LOAD_NAME" => Some(Opcode::LoadName),
            "STORE_NAME" => Some(Opcode::StoreName),
            "POP" => Some(Opcode::Pop),
            "ADD" => Some(Opcode::Add),
            "SUB" => Some(Opcode::Sub),
            "MUL" => Some(Opcode::Mul),
            "DIV" => Some(Opcode::Div),
            "EQUAL" => Some(Opcode::Equal),
            "GREATER" => Some(Opcode::Greater),
            "LESS" => Some(Opcode::Less),
            "NOT" => Some(Opcode::Not),
            "JUMP_FORWARD" => Some(Opcode::JumpForward),
            "JUMP_IF_FALSE" => Some(Opcode::JumpIfFalse),
            "JUMP_BACKWARD" => Some(Opcode::JumpBackward),
            "PRINT" => Some(Opcode::Print),
            "BUILD_LIST" => Some(Opcode::BuildList),
            "BUILD_MAP" => Some(Opcode::BuildMap),
            "ADD_TO_LIST" => Some(Opcode::AddToList),
            "MAP_SET" => Some(Opcode::MapSet),
            "GET_ITEM" => Some(Opcode::GetItem),
            "CALL_TASK" => Some(Opcode::CallTask),
            "RETURN" => Some(Opcode::Return),
            _ => None,
        }
    }

    pub fn from_u8(v: u8) -> Option<Self> {
        match v {
            1 => Some(Opcode::LoadConst),
            2 => Some(Opcode::LoadName),
            3 => Some(Opcode::StoreName),
            4 => Some(Opcode::Pop),
            5 => Some(Opcode::Add),
            6 => Some(Opcode::Sub),
            7 => Some(Opcode::Mul),
            8 => Some(Opcode::Div),
            9 => Some(Opcode::Equal),
            10 => Some(Opcode::Greater),
            11 => Some(Opcode::Less),
            12 => Some(Opcode::Not),
            13 => Some(Opcode::JumpForward),
            14 => Some(Opcode::JumpIfFalse),
            15 => Some(Opcode::JumpBackward),
            16 => Some(Opcode::Print),
            17 => Some(Opcode::BuildList),
            18 => Some(Opcode::BuildMap),
            19 => Some(Opcode::AddToList),
            20 => Some(Opcode::MapSet),
            21 => Some(Opcode::GetItem),
            22 => Some(Opcode::CallTask),
            23 => Some(Opcode::Return),
            _ => None,
        }
    }
}

impl TryFrom<&str> for Opcode {
    type Error = String;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        Opcode::from_str(value).ok_or_else(|| format!("Unknown opcode name: {}", value))
    }
}

impl TryFrom<u8> for Opcode {
    type Error = String;

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        Opcode::from_u8(value).ok_or_else(|| format!("Unknown opcode value: {}", value))
    }
}

impl Serialize for Opcode {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        serializer.serialize_str(self.as_str())
    }
}

impl<'de> Deserialize<'de> for Opcode {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct OpcodeVisitor;

        impl<'de> serde::de::Visitor<'de> for OpcodeVisitor {
            type Value = Opcode;

            fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
                formatter.write_str("an integer u8 opcode or string opcode name")
            }

            fn visit_u64<E>(self, value: u64) -> Result<Self::Value, E>
            where
                E: serde::de::Error,
            {
                Opcode::from_u8(value as u8)
                    .ok_or_else(|| serde::de::Error::custom(format!("invalid opcode integer: {}", value)))
            }

            fn visit_str<E>(self, value: &str) -> Result<Self::Value, E>
            where
                E: serde::de::Error,
            {
                Opcode::from_str(value)
                    .ok_or_else(|| serde::de::Error::custom(format!("invalid opcode name: {}", value)))
            }
        }

        deserializer.deserialize_any(OpcodeVisitor)
    }
}
