import unittest
import threading
from typing import Any, Dict
from aayu.runtime.kernel.interface import DispatchResult
from aayu.runtime.kernel.core import RuntimeKernel
from aayu.runtime.plugins.storage.runtime import StorageRuntime
import os

class TestStorageRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We will use an in-memory SQLite for testing isolation and speed
        os.environ["AAYU_ENV"] = "test"
        
    def setUp(self):
        self.kernel = RuntimeKernel()
        self.storage = StorageRuntime(in_memory=True)
        self.kernel.registry.register(self.storage)
        self.kernel.boot()
        
        # We must create a schema for testing
        schema = {
            "name": "User",
            "fields": [
                {"name": "id", "type": "Int", "primary_key": True},
                {"name": "name", "type": "String"},
                {"name": "age", "type": "Int"}
            ]
        }
        res = self.kernel.dispatch("storage", "migrate", {"schema": schema})
        self.assertTrue(res.success, msg=f"Migrate failed: {res.error}")

    def tearDown(self):
        self.kernel.shutdown()

    def test_insert_and_query(self):
        # Insert
        res_insert = self.kernel.dispatch("storage", "insert", {
            "model": "User",
            "data": {"id": 1, "name": "Ayush", "age": 20}
        })
        self.assertTrue(res_insert.success)
        self.assertEqual(res_insert.metadata.get("rows_affected"), 1)
        
        # Query
        res_query = self.kernel.dispatch("storage", "query", {
            "model": "User",
            "filters": {"id": 1}
        })
        self.assertTrue(res_query.success)
        self.assertEqual(len(res_query.data), 1)
        self.assertEqual(res_query.data[0]["name"], "Ayush")

    def test_update_and_delete(self):
        self.kernel.dispatch("storage", "insert", {
            "model": "User",
            "data": {"id": 1, "name": "Ayush", "age": 20}
        })
        
        # Update
        res_update = self.kernel.dispatch("storage", "update", {
            "model": "User",
            "filters": {"id": 1},
            "data": {"age": 21}
        })
        self.assertTrue(res_update.success)
        
        # Verify Update
        res_query = self.kernel.dispatch("storage", "query", {"model": "User", "filters": {"id": 1}})
        self.assertEqual(res_query.data[0]["age"], 21)
        
        # Delete
        res_delete = self.kernel.dispatch("storage", "delete", {
            "model": "User",
            "filters": {"id": 1}
        })
        self.assertTrue(res_delete.success)
        
        # Verify Delete
        res_query2 = self.kernel.dispatch("storage", "query", {"model": "User", "filters": {"id": 1}})
        self.assertEqual(len(res_query2.data), 0)

    def test_transactions_commit(self):
        res_tx = self.kernel.dispatch("storage", "transaction.begin", {})
        self.assertTrue(res_tx.success)
        tx_id = res_tx.data["transaction_id"]
        
        self.kernel.dispatch("storage", "insert", {
            "transaction_id": tx_id,
            "model": "User",
            "data": {"id": 2, "name": "Bob", "age": 30}
        })
        
        # Commit
        res_commit = self.kernel.dispatch("storage", "transaction.commit", {"transaction_id": tx_id})
        self.assertTrue(res_commit.success)
        
        # Verify committed
        res_query = self.kernel.dispatch("storage", "query", {"model": "User", "filters": {"id": 2}})
        self.assertEqual(len(res_query.data), 1)

    def test_transactions_rollback(self):
        res_tx = self.kernel.dispatch("storage", "transaction.begin", {})
        tx_id = res_tx.data["transaction_id"]
        
        self.kernel.dispatch("storage", "insert", {
            "transaction_id": tx_id,
            "model": "User",
            "data": {"id": 3, "name": "Charlie", "age": 40}
        })
        
        # Rollback
        res_rollback = self.kernel.dispatch("storage", "transaction.rollback", {"transaction_id": tx_id})
        self.assertTrue(res_rollback.success)
        
        # Verify rolled back
        res_query = self.kernel.dispatch("storage", "query", {"model": "User", "filters": {"id": 3}})
        self.assertEqual(len(res_query.data), 0)

    def test_invalid_schema_and_model(self):
        # Query invalid model
        res_query = self.kernel.dispatch("storage", "query", {"model": "NonExistent"})
        self.assertFalse(res_query.success)
        self.assertIsNotNone(res_query.error)
        
        # Insert invalid data
        res_insert = self.kernel.dispatch("storage", "insert", {
            "model": "User",
            "data": {"non_existent_column": "Test"}
        })
        self.assertFalse(res_insert.success)

    def test_concurrent_writes(self):
        def worker(uid):
            self.kernel.dispatch("storage", "insert", {
                "model": "User",
                "data": {"id": uid, "name": f"User_{uid}", "age": 20}
            })
            
        threads = [threading.Thread(target=worker, args=(i+100,)) for i in range(50)]
        for t in threads: t.start()
        for t in threads: t.join()
        
        res_query = self.kernel.dispatch("storage", "query", {"model": "User"})
        self.assertTrue(res_query.success)
        # 50 inserted by threads
        self.assertEqual(len(res_query.data), 50)

if __name__ == '__main__':
    unittest.main()
