use std::collections::HashMap;
use std::sync::{Arc, RwLock};

pub struct DbEngine {
    pub ram_store: Arc<RwLock<HashMap<String, String>>>,
    pub disk_path: String,
}

impl DbEngine {
    pub fn new(disk_path: &str) -> Self {
        // TODO: Load from SSD
        Self {
            ram_store: Arc::new(RwLock::new(HashMap::new())),
            disk_path: disk_path.to_string(),
        }
    }

    pub fn set(&self, key: &str, value: &str) {
        let mut store = self.ram_store.write().unwrap();
        store.insert(key.to_string(), value.to_string());
        // TODO: Flush to SSD / WAL
    }

    pub fn get(&self, key: &str) -> Option<String> {
        let store = self.ram_store.read().unwrap();
        store.get(key).cloned()
    }
}
