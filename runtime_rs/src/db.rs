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

// Recursive descent JSON parser for zero-dependency persistence
struct JsonParser<'a> {
    chars: std::iter::Peekable<std::str::Chars<'a>>,
}

impl<'a> JsonParser<'a> {
    fn new(input: &'a str) -> Self {
        Self {
            chars: input.chars().peekable(),
        }
    }

    fn skip_whitespace(&mut self) {
        while let Some(&c) = self.chars.peek() {
            if c.is_whitespace() {
                self.chars.next();
            } else {
                break;
            }
        }
    }

    fn parse_value(&mut self) -> Option<JsonValue> {
        self.skip_whitespace();
        let c = *self.chars.peek()?;
        match c {
            '"' => self.parse_string().map(JsonValue::String),
            '{' => self.parse_object().map(JsonValue::Object),
            '[' => self.parse_array().map(JsonValue::Array),
            't' | 'f' => self.parse_bool().map(JsonValue::Bool),
            'n' => self.parse_null().map(|_| JsonValue::Null),
            '-' | '0'..='9' => self.parse_number().map(JsonValue::Number),
            _ => None,
        }
    }

    fn parse_string(&mut self) -> Option<String> {
        if self.chars.next()? != '"' { return None; }
        let mut s = String::new();
        while let Some(c) = self.chars.next() {
            if c == '"' {
                return Some(s);
            } else if c == '\\' {
                let escaped = self.chars.next()?;
                match escaped {
                    '"' => s.push('"'),
                    '\\' => s.push('\\'),
                    '/' => s.push('/'),
                    'b' => s.push('\x08'),
                    'f' => s.push('\x0c'),
                    'n' => s.push('\n'),
                    'r' => s.push('\r'),
                    't' => s.push('\t'),
                    _ => s.push(escaped),
                }
            } else {
                s.push(c);
            }
        }
        None
    }

    fn parse_number(&mut self) -> Option<f64> {
        let mut s = String::new();
        while let Some(&c) = self.chars.peek() {
            if c == '-' || c == '+' || c == '.' || c.is_ascii_digit() || c == 'e' || c == 'E' {
                s.push(c);
                self.chars.next();
            } else {
                break;
            }
        }
        s.parse::<f64>().ok()
    }

    fn parse_bool(&mut self) -> Option<bool> {
        let mut s = String::new();
        while let Some(&c) = self.chars.peek() {
            if c.is_alphabetic() {
                s.push(c);
                self.chars.next();
            } else {
                break;
            }
        }
        match s.as_str() {
            "true" => Some(true),
            "false" => Some(false),
            _ => None,
        }
    }

    fn parse_null(&mut self) -> Option<()> {
        let mut s = String::new();
        while let Some(&c) = self.chars.peek() {
            if c.is_alphabetic() {
                s.push(c);
                self.chars.next();
            } else {
                break;
            }
        }
        if s == "null" { Some(()) } else { None }
    }

    fn parse_array(&mut self) -> Option<Vec<JsonValue>> {
        if self.chars.next()? != '[' { return None; }
        let mut arr = Vec::new();
        self.skip_whitespace();
        if let Some(&']') = self.chars.peek() {
            self.chars.next();
            return Some(arr);
        }
        loop {
            let val = self.parse_value()?;
            arr.push(val);
            self.skip_whitespace();
            match self.chars.next()? {
                ',' => continue,
                ']' => break,
                _ => return None,
            }
        }
        Some(arr)
    }

    fn parse_object(&mut self) -> Option<HashMap<String, JsonValue>> {
        if self.chars.next()? != '{' { return None; }
        let mut map = HashMap::new();
        self.skip_whitespace();
        if let Some(&'}') = self.chars.peek() {
            self.chars.next();
            return Some(map);
        }
        loop {
            self.skip_whitespace();
            let key = self.parse_string()?;
            self.skip_whitespace();
            if self.chars.next()? != ':' { return None; }
            let val = self.parse_value()?;
            map.insert(key, val);
            self.skip_whitespace();
            match self.chars.next()? {
                ',' => continue,
                '}' => break,
                _ => return None,
            }
        }
        Some(map)
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
            if file.read_to_string(&mut contents).is_ok() && !contents.trim().is_empty() {
                let mut parser = JsonParser::new(&contents);
                if let Some(JsonValue::Object(map)) = parser.parse_value() {
                    let mut store = self.ram_store.write().unwrap();
                    *store = map;
                }
            }
        }
    }

    pub fn flush_to_disk(&self) -> Result<(), std::io::Error> {
        let store = self.ram_store.read().unwrap();
        let mut file = OpenOptions::new()
            .create(true)
            .write(true)
            .truncate(true)
            .open(&self.disk_path)?;
        let mut lines = Vec::new();
        for (k, v) in store.iter() {
            lines.push(format!("\"{}\": {}", k.replace("\"", "\\\""), v));
        }
        let data = format!("{{\n{}\n}}", lines.join(",\n"));
        file.write_all(data.as_bytes())?;
        file.sync_all()?;
        Ok(())
    }

    pub fn set_json(&self, key: &str, value: JsonValue) {
        let mut store = self.ram_store.write().unwrap();
        store.insert(key.to_string(), value);
        drop(store);
        let _ = self.flush_to_disk();
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_db_persistence_roundtrip() {
        let temp_path = "test_persistence_db.rsdb";
        let _ = std::fs::remove_file(temp_path);

        {
            let db = DbEngine::new(temp_path);
            db.set("user", "alice");
            db.set("count", "42");
            db.set_json("tags", JsonValue::Array(vec![
                JsonValue::String("admin".into()),
                JsonValue::String("dev".into()),
            ]));
            let flush_res = db.flush_to_disk();
            assert!(flush_res.is_ok());
        }

        // Reopen DB from disk and verify persistence
        {
            let db = DbEngine::new(temp_path);
            assert_eq!(db.get("user"), Some("alice".to_string()));
            assert_eq!(db.get("count"), Some("42".to_string()));
            match db.get_json("tags") {
                Some(JsonValue::Array(arr)) => {
                    assert_eq!(arr.len(), 2);
                }
                _ => panic!("Expected array reloaded from disk"),
            }
        }

        let _ = std::fs::remove_file(temp_path);
    }
}
