import sqlite3
import os
from runtime.database.adapter.base import StorageAdapterBase

class SQLiteAdapter(StorageAdapterBase):
    def __init__(self, db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
    def create_table(self, table_name, fields):
        cols = []
        for name, type_str in fields.items():
            sql_type = "TEXT"
            if type_str == "Int": sql_type = "INTEGER"
            elif type_str == "Boolean": sql_type = "INTEGER"
            cols.append(f"{name} {sql_type}")
        
        # Default id column if not specified
        if "id" not in fields:
            cols.insert(0, "id INTEGER PRIMARY KEY AUTOINCREMENT")
            
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cols)});"
        self.execute_raw(sql)
        
    def execute_raw(self, sql, params=()):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor.fetchall()
        
    def execute_plan(self, plan):
        # Unpack the optimized plan to get the AST node
        ast = plan["plan"]["logical"]["ast"]
        node_type = type(ast).__name__
        
        if node_type == "InsertNode":
            fields = ast.fields
            cols = ", ".join(fields.keys())
            places = ", ".join(["?" for _ in fields])
            sql = f"INSERT INTO {ast.model_name} ({cols}) VALUES ({places});"
            self.execute_raw(sql, tuple(fields.values()))
            return {"status": "success", "operation": "insert"}
            
        elif node_type == "FindNode":
            sql = f"SELECT * FROM {ast.model_name};"
            rows = self.execute_raw(sql)
            return [dict(row) for row in rows]
            
        return None
