use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use std::fs::{File, OpenOptions};
use std::io::{Read, Write};
use std::path::Path;
use std::sync::atomic::{AtomicU64, Ordering};

static TEMP_FILE_ID: AtomicU64 = AtomicU64::new(0);

fn write_json_string(f: &mut std::fmt::Formatter<'_>, value: &str) -> std::fmt::Result {
    write!(f, "\"")?;
    for ch in value.chars() {
        match ch {
            '"' => write!(f, "\\\"")?,
            '\\' => write!(f, "\\\\")?,
            '\u{08}' => write!(f, "\\b")?,
            '\u{0c}' => write!(f, "\\f")?,
            '\n' => write!(f, "\\n")?,
            '\r' => write!(f, "\\r")?,
            '\t' => write!(f, "\\t")?,
            c if c <= '\u{1f}' => write!(f, "\\u{:04x}", c as u32)?,
            c => write!(f, "{}", c)?,
        }
    }
    write!(f, "\"")
}

#[cfg(not(windows))]
fn replace_file(temp: &Path, target: &Path) -> std::io::Result<()> {
    std::fs::rename(temp, target)
}

#[cfg(windows)]
fn replace_file(temp: &Path, target: &Path) -> std::io::Result<()> {
    use std::os::windows::ffi::OsStrExt;
    use std::io;
    #[link(name = "Kernel32")]
    unsafe extern "system" {
        fn MoveFileExW(existing: *const u16, new: *const u16, flags: u32) -> i32;
    }
    const MOVEFILE_REPLACE_EXISTING: u32 = 0x1;
    const MOVEFILE_WRITE_THROUGH: u32 = 0x8;
    let from: Vec<u16> = temp.as_os_str().encode_wide().chain(Some(0)).collect();
    let to: Vec<u16> = target.as_os_str().encode_wide().chain(Some(0)).collect();
    let ok = unsafe { MoveFileExW(from.as_ptr(), to.as_ptr(), MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH) };
    if ok == 0 { Err(io::Error::last_os_error()) } else { Ok(()) }
}

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
            JsonValue::Number(n) if n.is_finite() => write!(f, "{}", n),
            JsonValue::Number(_) => write!(f, "null"),
            JsonValue::String(s) => write_json_string(f, s),
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
                    write_json_string(f, k)?;
                    write!(f, ":{}", v)?;
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
                    'u' => {
                        let first = self.parse_hex4()?;
                        let codepoint = if (0xD800..=0xDBFF).contains(&first) {
                            if self.chars.next()? != '\\' || self.chars.next()? != 'u' { return None; }
                            let second = self.parse_hex4()?;
                            if !(0xDC00..=0xDFFF).contains(&second) { return None; }
                            0x10000 + (((first - 0xD800) as u32) << 10) + (second - 0xDC00) as u32
                        } else if (0xDC00..=0xDFFF).contains(&first) {
                            return None;
                        } else { first as u32 };
                        s.push(char::from_u32(codepoint)?);
                    }
                    _ => return None,
                }
            } else {
                s.push(c);
            }
        }
        None
    }

    fn parse_hex4(&mut self) -> Option<u16> {
        let mut value = 0u16;
        for _ in 0..4 {
            value = value.checked_mul(16)? + self.chars.next()?.to_digit(16)? as u16;
        }
        Some(value)
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
        let data = JsonValue::Object(store.clone()).to_string();
        let target = Path::new(&self.disk_path);
        let id = TEMP_FILE_ID.fetch_add(1, Ordering::Relaxed);
        let file_name = target.file_name().ok_or_else(|| std::io::Error::new(std::io::ErrorKind::InvalidInput, "database path has no filename"))?;
        let temp_name = format!("{}.tmp-{}-{}", file_name.to_string_lossy(), std::process::id(), id);
        let temp = target.with_file_name(temp_name);
        let mut file = OpenOptions::new().create_new(true).write(true).open(&temp)?;
        let result = (|| {
            file.write_all(data.as_bytes())?;
            file.sync_all()?;
            drop(file);
            replace_file(&temp, target)?;
            #[cfg(unix)]
            {
                let parent = target
                    .parent()
                    .filter(|parent| !parent.as_os_str().is_empty())
                    .unwrap_or(Path::new("."));
                File::open(parent)?.sync_all()?;
            }
            Ok(())
        })();
        if result.is_err() { let _ = std::fs::remove_file(&temp); }
        result
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
            db.set("key\"\\\n", "value\"\\\n\t\u{0001}");
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
            assert_eq!(db.get("key\"\\\n"), Some("value\"\\\n\t\u{0001}".to_string()));
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
