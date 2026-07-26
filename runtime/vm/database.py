import sqlite3
import os

class DatabaseEngine:
    def __init__(self, db_path="db.sqlite3"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.models = {}

    def create_model(self, model_name: str, fields: list, decorators: list = None):
        table_name = model_name.lower() + "s"
        if not table_name.endswith('s'): table_name += "s"
        
        decorators = decorators or []
        dec_names = [d["name"] for d in decorators] if decorators and isinstance(decorators[0], dict) else decorators
        is_secure = any(d in dec_names for d in ["auth", "admin", "role", "permission", "secure"])
        
        roles = []
        permissions = []
        is_soft_delete = "soft_delete" in dec_names
        is_owner = "owner" in dec_names
        
        for d in decorators:
            if isinstance(d, dict):
                args = d.get("args", [])
                val_args = []
                for a in args:
                    if hasattr(a, "value"): val_args.append(a.value)
                    else: val_args.append(str(a))
                    
                if d["name"] == "role":
                    roles.extend(val_args)
                elif d["name"] == "permission":
                    permissions.extend(val_args)
        
        columns = [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
            "updated_at DATETIME DEFAULT CURRENT_TIMESTAMP"
        ]
        
        parsed_fields = {}
        for f in fields:
            name = f["name"]
            f_type = f["type"]
            attributes = f.get("attributes", [])
            
            sql_type = "TEXT"
            if f_type in ["Int", "Boolean"]: sql_type = "INTEGER"
            elif f_type == "Float": sql_type = "REAL"
            
            # Map implicit base types for advanced types
            implicit_regex = None
            if f_type == "Email":
                implicit_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            elif f_type == "Phone":
                implicit_regex = r"^\+?[0-9\s\-\(\)]+$"
            elif f_type == "URL":
                implicit_regex = r"^https?:\/\/.*$"
            elif f_type == "UUID":
                implicit_regex = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
            
            schema = {
                "type": f_type,
                "required": False,
                "nullable": True,
                "unique": False,
                "min": None,
                "max": None,
                "regex": implicit_regex,
                "default": None,
                "enum": None
            }
            
            constraints = []
            for attr in attributes:
                attr_name = attr.name if hasattr(attr, 'name') else attr.get("name", "")
                args = attr.args if hasattr(attr, 'args') else attr.get("args", [])
                
                # Extract literal values from args
                val_args = []
                for a in args:
                    if hasattr(a, "value"): val_args.append(a.value)
                    else: val_args.append(a)
                    
                if attr_name == "unique":
                    constraints.append("UNIQUE")
                    schema["unique"] = True
                elif attr_name == "primary":
                    constraints.append("PRIMARY KEY")
                elif attr_name == "required":
                    constraints.append("NOT NULL")
                    schema["required"] = True
                    schema["nullable"] = False
                elif attr_name == "nullable":
                    schema["nullable"] = True
                    schema["required"] = False
                elif attr_name == "min" and val_args:
                    schema["min"] = val_args[0]
                elif attr_name == "max" and val_args:
                    schema["max"] = val_args[0]
                elif attr_name == "regex" and val_args:
                    schema["regex"] = val_args[0]
                elif attr_name == "default" and val_args:
                    schema["default"] = val_args[0]
                    # Also map to SQL DEFAULT
                    val = val_args[0]
                    if val == "now" and sql_type == "TEXT":
                        constraints.append("DEFAULT CURRENT_TIMESTAMP")
                    elif isinstance(val, (int, float)):
                        constraints.append(f"DEFAULT {val}")
                    elif isinstance(val, str):
                        constraints.append(f"DEFAULT '{val}'")
                elif attr_name == "enum" and val_args:
                    schema["enum"] = val_args
                    
            col_def = f"{name} {sql_type}"
            if constraints:
                col_def += " " + " ".join(constraints)
            columns.append(col_def)
            parsed_fields[name] = schema
            
            
        columns_str = ", ".join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str});"
        self.cursor.execute(query)
        self.conn.commit()
        
        self.models[model_name] = {
            "table": table_name,
            "fields": parsed_fields,
            "primary_key": "id",
            "secure": is_secure,
            "roles": roles,
            "permissions": permissions,
            "owner": is_owner,
            "timestamps": True,
            "soft_delete": is_soft_delete
        }
        
        print(f"[DB] Registered model '{model_name}' -> table '{table_name}' (Secure: {is_secure})")

    def execute_query(self, query: str, params=()):
        self.cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT") or "RETURNING" in query.upper():
            results = [dict(row) for row in self.cursor.fetchall()]
            self.conn.commit()
            return results
        self.conn.commit()
        return []
        
    def _build_where(self, model_name, filters):
        if not filters:
            return "", []
        clauses = []
        params = []
        for k, v in filters.items():
            if k in ["page", "limit", "offset", "sort", "order", "q"]:
                continue
            
            # Handle ?age>18 parsed as k="age>18", v="" OR k="age", v=">18"
            if ">" in v:
                clauses.append(f"{k} > ?")
                params.append(v.replace(">", ""))
            elif "<" in v:
                clauses.append(f"{k} < ?")
                params.append(v.replace("<", ""))
            elif "~" in v:
                clauses.append(f"{k} LIKE ?")
                params.append(f"%{v.replace('~', '')}%")
            elif ">" in k:
                f, val = k.split(">", 1)
                clauses.append(f"{f} > ?")
                params.append(val or v)
            elif "<" in k:
                f, val = k.split("<", 1)
                clauses.append(f"{f} < ?")
                params.append(val or v)
            elif "~" in k:
                f, val = k.split("~", 1)
                clauses.append(f"{f} LIKE ?")
                params.append(f"%{val or v}%")
            else:
                clauses.append(f"{k} = ?")
                params.append(v)
                
        if "q" in filters and model_name in self.models:
            q_val = filters["q"]
            fields = self.models[model_name]["fields"]
            text_fields = [f for f, data in fields.items() if data["type"] == "text"]
            if text_fields:
                q_clauses = " OR ".join([f"{f} LIKE ?" for f in text_fields])
                if clauses:
                    clauses = [f"({' AND '.join(clauses)}) AND ({q_clauses})"]
                else:
                    clauses = [q_clauses]
                params.extend([f"%{q_val}%"] * len(text_fields))
            
        if not clauses: return "", []
        return " WHERE " + " AND ".join(clauses), params

    def insert(self, model_name: str, data: dict):
        table = self.models[model_name]["table"]
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
        res = self.execute_query(query, tuple(data.values()))
        return res[0] if res else None

    def find(self, model_name: str, filters: dict = None):
        table = self.models[model_name]["table"]
        where_clause, params = self._build_where(model_name, filters)
        
        query = f"SELECT * FROM {table}{where_clause}"
        
        if filters:
            sort = filters.get("sort")
            order = filters.get("order", "asc")
            if sort:
                if sort.startswith("-"):
                    sort = sort[1:]
                    order = "desc"
                query += f" ORDER BY {sort} {order}"
                
            limit = filters.get("limit", 20)
            offset = filters.get("offset", (int(filters.get("page", 1)) - 1) * int(limit))
            query += f" LIMIT {int(limit)} OFFSET {int(offset)}"
            
        return self.execute_query(query, tuple(params))

    def find_one(self, model_name: str, id: int):
        table = self.models[model_name]["table"]
        res = self.execute_query(f"SELECT * FROM {table} WHERE id = ?", (id,))
        return res[0] if res else None

    def update(self, model_name: str, id: int, data: dict):
        table = self.models[model_name]["table"]
        set_clauses = ", ".join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clauses}, updated_at = CURRENT_TIMESTAMP WHERE id = ? RETURNING *"
        params = list(data.values()) + [id]
        res = self.execute_query(query, tuple(params))
        return res[0] if res else None

    def delete(self, model_name: str, id: int):
        table = self.models[model_name]["table"]
        self.execute_query(f"DELETE FROM {table} WHERE id = ?", (id,))
        return True

    def count(self, model_name: str, filters: dict = None):
        table = self.models[model_name]["table"]
        where_clause, params = self._build_where(model_name, filters)
        res = self.execute_query(f"SELECT COUNT(*) as c FROM {table}{where_clause}", tuple(params))
        return res[0]["c"] if res else 0

    def exists(self, model_name: str, id: int):
        table = self.models[model_name]["table"]
        res = self.execute_query(f"SELECT 1 FROM {table} WHERE id = ?", (id,))
        return len(res) > 0
