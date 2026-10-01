use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use std::fs::{File, OpenOptions};
use std::io::{Read, Write};

#[derive(Debug, Clone)]
pub enum JsonValue {
    Null,
    Bool(bool),
    Number(f64),
    String(String),
    Array(Vec<JsonValue>),
    Object(HashMap<String, JsonValue>),
}

impl std::fmt::Display for JsonValue {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            JsonValue::Null => write!(f, "null"),
            JsonValue::Bool(b) => write!(f, "{}", b),
            JsonValue::Number(n) => write!(f, "{}", n),
            JsonValue::String(s) => write!(f, "\"{}\"", s.replace("\"", "\\\"")),
            JsonValue::Array(arr) => {
                write!(f, "[")?;
                for (i, item) in arr.iter().enumerate() {
                    if i > 0 { write!(f, ",")?; }
                    write!(f, "{}", item)?;
                }
                write!(f, "]")
            },
            JsonValue::Object(obj) => {
                write!(f, "{{")?;
                let mut first = true;
                for (k, v) in obj {
                    if !first { write!(f, ",")?; }
                    write!(f, "\"{}\":{}", k.replace("\"", "\\\""), v)?;
                    first = false;
                }
                write!(f, "}}")
            }
        }
    }
}

pub struct DbEngine {
    pub ram_store: Arc<RwLock<HashMap<String, JsonValue>>>,
    pub disk_path: String,
}

impl DbEngine {
    pub fn new(disk_path: &str) -> Self {
        let mut db = Self {
            ram_store: Arc::new(RwLock::new(HashMap::new())),
            disk_path: disk_path.to_string(),
        };
        db.load_from_disk();
        db
    }

    fn load_from_disk(&mut self) {
        if let Ok(mut file) = File::open(&self.disk_path) {
            let mut contents = String::new();
            if file.read_to_string(&mut contents).is_ok() {
                // Here we would parse JSON, but this is a mock implementation
            }
        }
    }

    pub fn flush_to_disk(&self) {
        let store = self.ram_store.read().unwrap();
        if let Ok(mut file) = OpenOptions::new().create(true).write(true).truncate(true).open(&self.disk_path) {
            let mut lines = Vec::new();
            for (k, v) in store.iter() {
                lines.push(format!("\"{}\": {}", k, v));
            }
            let data = format!("{{\n{}\n}}", lines.join(",\n"));
            let _ = file.write_all(data.as_bytes());
        }
    }

    pub fn set_json(&self, key: &str, value: JsonValue) {
        let mut store = self.ram_store.write().unwrap();
        store.insert(key.to_string(), value);
        drop(store);
        self.flush_to_disk();
    }

    pub fn get_json(&self, key: &str) -> Option<JsonValue> {
        let store = self.ram_store.read().unwrap();
        store.get(key).cloned()
    }

    // Legacy string support
    pub fn set(&self, key: &str, value: &str) {
        let val = if value == "null" {
            JsonValue::Null
        } else if value == "true" {
            JsonValue::Bool(true)
        } else if value == "false" {
            JsonValue::Bool(false)
        } else if let Ok(n) = value.parse::<f64>() {
            JsonValue::Number(n)
        } else {
            JsonValue::String(value.to_string())
        };
        self.set_json(key, val);
    }

    pub fn get(&self, key: &str) -> Option<String> {
        self.get_json(key).map(|v| match v {
            JsonValue::String(s) => s,
            _ => v.to_string(),
        })
    }
}
