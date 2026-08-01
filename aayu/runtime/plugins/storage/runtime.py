import time
import uuid
import sqlite3
import os
import logging
from typing import Any, Dict
from aayu.runtime.kernel.interface import RuntimeInterface, RuntimeMetadata, DispatchResult

logger = logging.getLogger("aayu.kernel.storage")

class StorageRuntime(RuntimeInterface):
    """
    AAYU OS - Storage Runtime Plugin.
    Provides OS-level CRUD and Transaction capabilities.
    Wraps legacy database logic into the modern Plugin architecture.
    """
    def __init__(self, in_memory: bool = False, db_path: str = "aayu_data/Main.db"):
        self.in_memory = in_memory
        self.db_path = ":memory:" if in_memory else db_path
        self.conn = None
        self.kernel = None

    def metadata(self) -> RuntimeMetadata:
        return RuntimeMetadata(
            name="storage",
            version="1.0",
            dependencies=[],
            author="AAYU Core",
            priority=20
        )

    def initialize(self, kernel) -> None:
        self.kernel = kernel

    def boot(self) -> None:
        if not self.in_memory:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        # Check_same_thread=False allows us to share connection in threads, 
        # but we must manage our own locks if we use a single connection for concurrent writes.
        # For full thread safety in tests we enable WAL or use isolation.
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        if not self.in_memory:
            self.conn.execute("PRAGMA journal_mode=WAL;")
        
        logger.info(f"Storage Runtime booted (in_memory={self.in_memory})")

    def start(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def _execute(self, sql: str, params: tuple = (), commit: bool = False, transaction_id: str = None) -> Any:
        # If transaction_id is provided, we should technically route to a specific connection/cursor.
        # For simplicity in this sqlite wrapper, we just execute.
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        if commit:
            self.conn.commit()
        
        rows_affected = cursor.rowcount
        
        # If it's a SELECT, return rows
        if sql.strip().upper().startswith("SELECT"):
            return [dict(r) for r in cursor.fetchall()], rows_affected
        else:
            return None, rows_affected

    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        start_ms = time.time()
        try:
            if action == "migrate":
                # Create table
                schema = payload["schema"]
                table_name = schema["name"]
                cols = []
                for field in schema["fields"]:
                    fname = field["name"]
                    ftype = field["type"]
                    sql_type = "TEXT"
                    if ftype == "Int": sql_type = "INTEGER"
                    elif ftype == "Boolean": sql_type = "INTEGER"
                    
                    if field.get("primary_key"):
                        sql_type += " PRIMARY KEY"
                    cols.append(f"{fname} {sql_type}")
                
                sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cols)});"
                self._execute(sql, commit=True)
                return DispatchResult(success=True, time=time.time() - start_ms)

            elif action == "insert":
                model = payload["model"]
                data = payload["data"]
                cols = ", ".join(data.keys())
                places = ", ".join(["?" for _ in data])
                sql = f"INSERT INTO {model} ({cols}) VALUES ({places});"
                
                # If inside transaction, don't auto-commit
                commit = "transaction_id" not in payload
                _, rows_affected = self._execute(sql, tuple(data.values()), commit=commit)
                
                return DispatchResult(success=True, metadata={"rows_affected": rows_affected}, time=time.time() - start_ms)

            elif action == "update":
                model = payload["model"]
                filters = payload["filters"]
                data = payload["data"]
                
                set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
                where_clause = " AND ".join([f"{k} = ?" for k in filters.keys()])
                
                sql = f"UPDATE {model} SET {set_clause} WHERE {where_clause};"
                params = tuple(data.values()) + tuple(filters.values())
                
                commit = "transaction_id" not in payload
                _, rows_affected = self._execute(sql, params, commit=commit)
                
                return DispatchResult(success=True, metadata={"rows_affected": rows_affected}, time=time.time() - start_ms)

            elif action == "delete":
                model = payload["model"]
                filters = payload["filters"]
                
                where_clause = " AND ".join([f"{k} = ?" for k in filters.keys()])
                sql = f"DELETE FROM {model} WHERE {where_clause};"
                
                commit = "transaction_id" not in payload
                _, rows_affected = self._execute(sql, tuple(filters.values()), commit=commit)
                
                return DispatchResult(success=True, metadata={"rows_affected": rows_affected}, time=time.time() - start_ms)

            elif action == "query":
                model = payload["model"]
                filters = payload.get("filters", {})
                
                sql = f"SELECT * FROM {model}"
                params = ()
                if filters:
                    where_clause = " AND ".join([f"{k} = ?" for k in filters.keys()])
                    sql += f" WHERE {where_clause}"
                    params = tuple(filters.values())
                    
                rows, _ = self._execute(sql, params)
                return DispatchResult(success=True, data=rows, time=time.time() - start_ms)

            elif action == "transaction.begin":
                tx_id = str(uuid.uuid4())
                self._execute("BEGIN TRANSACTION;")
                return DispatchResult(success=True, data={"transaction_id": tx_id}, time=time.time() - start_ms)

            elif action == "transaction.commit":
                self._execute("COMMIT;")
                return DispatchResult(success=True, time=time.time() - start_ms)

            elif action == "transaction.rollback":
                self._execute("ROLLBACK;")
                return DispatchResult(success=True, time=time.time() - start_ms)

            else:
                raise ValueError(f"Unknown Storage action: {action}")

        except sqlite3.OperationalError as e:
            return DispatchResult(success=False, error=f"Database error: {str(e)}", time=time.time() - start_ms)
        except Exception as e:
            return DispatchResult(success=False, error=str(e), time=time.time() - start_ms)

    def stop(self) -> None:
        pass

    def shutdown(self) -> None:
        if self.conn:
            self.conn.close()

    def health(self) -> dict:
        return {"status": "healthy"}

    def capabilities(self) -> dict:
        return {"actions": ["migrate", "insert", "update", "delete", "query", "transaction.begin", "transaction.commit", "transaction.rollback"]}
    
    def diagnostics(self) -> dict:
        return {}
