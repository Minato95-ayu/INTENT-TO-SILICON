import pytest
from runtime.database.runtime import DatabaseRuntime

def test_database_runtime_e2e():
    metadata = {
        "data_ir": {
            "storages": [{"name": "app.db"}],
            "models": [{"name": "User", "fields": [{"name": "id", "type": "Int", "is_primary": True}]}]
        }
    }
    rt = DatabaseRuntime(metadata)
    rt.initialize()
    rt.start()
    
    assert rt.engine is not None

