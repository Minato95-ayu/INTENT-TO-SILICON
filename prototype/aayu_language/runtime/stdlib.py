import os
import datetime
import sqlite3
import json
import re

# Import response types from interpreter if needed, or define them locally
try:
    from interpreter import AayuJSONResponse, AayuHTMLResponse, AayuTextResponse
except ImportError:
    class AayuJSONResponse:
        def __init__(self, data_str):
            self.data_str = data_str

    class AayuHTMLResponse:
        def __init__(self, data_str):
            self.data_str = data_str

    class AayuTextResponse:
        def __init__(self, data_str):
            self.data_str = data_str

class StdLib:
    def __init__(self, vm):
        self.vm = vm

    def db_register_entity(self, name: str, fields: list):
        """Creates table and stores schema metadata in SQLite."""
        # 1. Create metadata table and insert schema rows
        self.vm.db_cursor.execute(
            "CREATE TABLE IF NOT EXISTS _aayu_schema (entity_name TEXT, field_name TEXT, field_type TEXT)"
        )
        self.vm.db_cursor.execute(
            "DELETE FROM _aayu_schema WHERE entity_name = ?", (name,)
        )
        for field in fields:
            field_name = field["name"]
            field_type = field["type"]
            self.vm.db_cursor.execute(
                "INSERT INTO _aayu_schema (entity_name, field_name, field_type) VALUES (?, ?, ?)",
                (name, field_name, field_type)
            )

        # 2. Create the actual entity table
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
        for field in fields:
            field_name = field["name"]
            field_type = field["type"]
            if field_type == "text":
                columns.append(f"{field_name} TEXT")
            elif field_type == "number":
                columns.append(f"{field_name} REAL")
            else:
                columns.append(f"{field_name} TEXT")
        columns.append("created_at TEXT")
        columns.append("updated_at TEXT")
        
        sql = f"CREATE TABLE IF NOT EXISTS {name} ({', '.join(columns)})"
        self.vm.db_cursor.execute(sql)
        self.vm.db_conn.commit()

    def db_create(self, entity_name: str, data_map: dict):
        """Inserts a new record into the database table."""
        if not isinstance(data_map, dict):
            raise Exception(f"Create target must be a map, got: {type(data_map)}")
            
        now = datetime.datetime.now().isoformat()
        
        insert_data = dict(data_map)
        insert_data["created_at"] = now
        insert_data["updated_at"] = now
        
        columns = list(insert_data.keys())
        placeholders = ["?"] * len(columns)
        values = list(insert_data.values())
        
        sql = f"INSERT INTO {entity_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        self.vm.db_cursor.execute(sql, values)
        self.vm.db_conn.commit()

    def db_find(self, entity_name: str, condition_field: str = None, condition_value = None) -> list:
        """Selects records matching condition, or all if no condition."""
        if condition_field:
            sql = f"SELECT * FROM {entity_name} WHERE {condition_field} = ?"
            self.vm.db_cursor.execute(sql, [condition_value])
        else:
            sql = f"SELECT * FROM {entity_name}"
            self.vm.db_cursor.execute(sql)
            
        rows = self.vm.db_cursor.fetchall()
        result = []
        for row in rows:
            result.append(dict(row))
        return result

    def db_update(self, entity_name: str, condition_field: str, condition_value, data_map: dict):
        """Updates records matching condition."""
        if not isinstance(data_map, dict):
            raise Exception(f"Update payload must be a map, got: {type(data_map)}")
            
        now = datetime.datetime.now().isoformat()
        update_data = dict(data_map)
        update_data["updated_at"] = now
        
        set_clauses = [f"{k} = ?" for k in update_data.keys()]
        values = list(update_data.values())
        values.append(condition_value)
        
        sql = f"UPDATE {entity_name} SET {', '.join(set_clauses)} WHERE {condition_field} = ?"
        self.vm.db_cursor.execute(sql, values)
        self.vm.db_conn.commit()

    def db_delete(self, entity_name: str, condition_field: str, condition_value):
        """Deletes records matching condition."""
        sql = f"DELETE FROM {entity_name} WHERE {condition_field} = ?"
        self.vm.db_cursor.execute(sql, [condition_value])
        self.vm.db_conn.commit()

    def json_serialize(self, data) -> AayuJSONResponse:
        """Serializes data to JSON response."""
        try:
            json_str = json.dumps(data)
            return AayuJSONResponse(json_str)
        except TypeError:
            raise Exception("Cannot serialize data to JSON.")

    def render_template(self, template_path: str, context_map: dict = None) -> str:
        """Loads and renders template file using context map variables."""
        if not os.path.exists(template_path):
            raise Exception(f"Template file '{template_path}' not found.")
            
        with open(template_path, 'r', encoding='utf-8') as f:
            template_str = f.read()
            
        if context_map and isinstance(context_map, dict):
            for key, val in context_map.items():
                pattern = r'\{\{\s*' + re.escape(key) + r'\s*\}\}'
                template_str = re.sub(pattern, str(val), template_str)
                
        # Strip missing variables placeholders
        template_str = re.sub(r'\{\{\s*[\w_]+\s*\}\}', '', template_str)
        return template_str
