from runtime.base import BaseRuntime
from runtime.database.engine import StorageEngine

class DatabaseRuntime(BaseRuntime):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.engine = None

    def initialize(self):
        data_ir = self.metadata.get("data_ir", {})
        
        # Determine adapter, currently fixed to SQLite
        # Note: 'storages' has db info, 'models' has schema info
        self.engine = StorageEngine(data_ir)
        self.engine.initialize()

    def start(self):
        self.engine.start()
