class TransactionManager:
    def __init__(self, adapter):
        self.adapter = adapter
    
    def begin(self):
        self.adapter.execute_raw("BEGIN TRANSACTION;")
        
    def commit(self):
        self.adapter.execute_raw("COMMIT;")
        
    def rollback(self):
        self.adapter.execute_raw("ROLLBACK;")
