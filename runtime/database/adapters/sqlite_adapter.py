import sqlite3
import os
from typing import Dict, Any

class SQLiteAdapter:
    """
    Native SQLite Database Adapter for AAYU.
    """
    def __init__(self, db_name: str, models: list):
        self.db_name = db_name
        self.models = models
        self.conn = None

    def initialize(self):
        os.makedirs("aayu_data", exist_ok=True)
        db_path = os.path.join("aayu_data", f"{self.db_name}.db")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._auto_migrate()

    def _auto_migrate(self):
        """
        Dynamically create tables based on models.
        """
        cursor = self.conn.cursor()
        
        type_mapping = {
            "Int": "INTEGER",
            "String": "TEXT",
            "Boolean": "INTEGER",
            "number": "REAL",
            "text": "TEXT"
        }

        for model in self.models:
            table_name = model["name"]
            fields = []
            
            has_id = False
            for field in model["fields"]:
                fname = field["name"]
                ftype = field["type"]
                # For simplicity, treat arrays as TEXT (JSON stringified) for SQLite
                if ftype.endswith("[]"):
                    ftype = ftype[:-2]
                    sql_type = "TEXT"
                else:
                    sql_type = type_mapping.get(ftype, "TEXT")
                
                line = f"{fname} {sql_type}"
                if fname == "id" and not has_id:
                    if sql_type == "INTEGER":
                        line += " PRIMARY KEY AUTOINCREMENT"
                    else:
                        line += " PRIMARY KEY"
                    has_id = True
                
                fields.append(line)
                
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(fields)});"
            cursor.execute(query)
            
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
