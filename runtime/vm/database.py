# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import sqlite3
import os

class DatabaseEngine:
    __slots__ = ['_conn', '_cursor', 'db_path', 'models']

    def __init__(self, db_path='db.sqlite3'):
        self.db_path = db_path
        self._conn = None
        self._cursor = None
        self.models = {}

    @property
    def conn(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self.conn.cursor()
        return self._cursor

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None
            self._cursor = None

    def create_model(self, model_name: str, fields: list, decorators: list=None):
        table_name = model_name.lower() + 's'
        if not table_name.endswith('s'):
            table_name += 's'
        is_secure = False
        roles = []
        permissions = []
        is_owner = False
        is_soft_delete = False
        if decorators:
            for dec in decorators:
                if dec.name == 'Secure':
                    is_secure = True
                    for arg in dec.args:
                        if hasattr(arg, 'name') and arg.name == 'roles':
                            if hasattr(arg, 'value') and isinstance(arg.value, list):
                                roles = [v.value for v in arg.value]
                            elif isinstance(arg.value, list):
                                roles = arg.value
                        elif isinstance(arg, dict) and 'roles' in arg:
                            roles = arg['roles']
                        elif hasattr(arg, 'name') and arg.name == 'permissions':
                            if hasattr(arg, 'value') and isinstance(arg.value, list):
                                permissions = [v.value for v in arg.value]
                        elif isinstance(arg, dict) and 'permissions' in arg:
                            permissions = arg['permissions']
                        elif hasattr(arg, 'name') and arg.name == 'owner' and (arg.value is True):
                            is_owner = True
                        elif isinstance(arg, dict) and arg.get('owner') is True:
                            is_owner = True
                elif dec.name == 'SoftDelete':
                    is_soft_delete = True
        columns = ['id INTEGER PRIMARY KEY AUTOINCREMENT']
        if is_soft_delete:
            columns.append('deleted_at DATETIME DEFAULT NULL')
        columns.append('created_at DATETIME DEFAULT CURRENT_TIMESTAMP')
        columns.append('updated_at DATETIME DEFAULT CURRENT_TIMESTAMP')
        parsed_fields = {}
        for field in fields:
            name = field.name if hasattr(field, 'name') else field.get('name')
            type_info = field.type if hasattr(field, 'type') else field.get('type')
            f_type = type_info.name if hasattr(type_info, 'name') else type_info
            attributes = field.attributes if hasattr(field, 'attributes') else field.get('attributes', [])
            sql_type = 'TEXT'
            if f_type == 'Int':
                sql_type = 'INTEGER'
            elif f_type == 'Float':
                sql_type = 'REAL'
            elif f_type == 'Boolean':
                sql_type = 'INTEGER'
            elif f_type == 'DateTime':
                sql_type = 'DATETIME'
            elif f_type == 'Email' or f_type == 'URL' or f_type == 'Phone':
                sql_type = 'TEXT'
            elif f_type == 'UUID':
                sql_type = 'TEXT'
            implicit_regex = None
            if f_type == 'Email':
                implicit_regex = '^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'
            elif f_type == 'Phone':
                implicit_regex = '^\\+?[0-9\\s\\-\\(\\)]+$'
            elif f_type == 'URL':
                implicit_regex = '^https?:\\/\\/.*$'
            elif f_type == 'UUID':
                implicit_regex = '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            schema = {'type': f_type, 'required': False, 'nullable': True, 'unique': False, 'min': None, 'max': None, 'regex': implicit_regex, 'default': None, 'enum': None}
            constraints = []
            for attr in attributes:
                attr_name = attr.name if hasattr(attr, 'name') else attr.get('name', '')
                args = attr.args if hasattr(attr, 'args') else attr.get('args', [])
                val_args = []
                for a in args:
                    if hasattr(a, 'value'):
                        val_args.append(a.value)
                    else:
                        val_args.append(a)
                if attr_name == 'unique':
                    constraints.append('UNIQUE')
                    schema['unique'] = True
                elif attr_name == 'primary':
                    constraints.append('PRIMARY KEY')
                elif attr_name == 'required':
                    constraints.append('NOT NULL')
                    schema['required'] = True
                    schema['nullable'] = False
                elif attr_name == 'nullable':
                    schema['nullable'] = True
                    schema['required'] = False
                elif attr_name == 'min' and val_args:
                    schema['min'] = val_args[0]
                elif attr_name == 'max' and val_args:
                    schema['max'] = val_args[0]
                elif attr_name == 'regex' and val_args:
                    schema['regex'] = val_args[0]
                elif attr_name == 'default' and val_args:
                    schema['default'] = val_args[0]
                    val = val_args[0]
                    if val == 'now' and sql_type == 'TEXT':
                        constraints.append('DEFAULT CURRENT_TIMESTAMP')
                    elif isinstance(val, (int, float)):
                        constraints.append(f'DEFAULT {val}')
                    elif isinstance(val, str):
                        constraints.append(f"DEFAULT '{val}'")
                elif attr_name == 'enum' and val_args:
                    schema['enum'] = val_args
            col_def = f'{name} {sql_type}'
            if constraints:
                col_def += ' ' + ' '.join(constraints)
            columns.append(col_def)
            parsed_fields[name] = schema
        columns_str = ', '.join(columns)
        query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str});'
        self.cursor.execute(query)
        self.conn.commit()
        self.models[model_name] = {'table': table_name, 'fields': parsed_fields, 'primary_key': 'id', 'secure': is_secure, 'roles': roles, 'permissions': permissions, 'owner': is_owner, 'timestamps': True, 'soft_delete': is_soft_delete}
        print(f"[DB] Registered model '{model_name}' -> table '{table_name}' (Secure: {is_secure})")

    def execute_query(self, query: str, params=()):
        self.cursor.execute(query, params)
        if query.strip().upper().startswith('SELECT') or 'RETURNING' in query.upper():
            results = [dict(row) for row in self.cursor.fetchall()]
            self.conn.commit()
            return results
        self.conn.commit()
        return []

    def _build_where(self, model_name, filters):
        if not filters:
            return ('', [])
        clauses = []
        params = []
        for k, v in filters.items():
            if k in ['page', 'limit', 'offset', 'sort', 'order', 'q']:
                continue
            if '>' in v:
                clauses.append(f'{k} > ?')
                params.append(v.replace('>', ''))
            elif '<' in v:
                clauses.append(f'{k} < ?')
                params.append(v.replace('<', ''))
            elif '~' in v:
                clauses.append(f'{k} LIKE ?')
                params.append(f"%{v.replace('~', '')}%")
            elif '>' in k:
                f, val = k.split('>', 1)
                clauses.append(f'{f} > ?')
                params.append(val or v)
            elif '<' in k:
                f, val = k.split('<', 1)
                clauses.append(f'{f} < ?')
                params.append(val or v)
            elif '~' in k:
                f, val = k.split('~', 1)
                clauses.append(f'{f} LIKE ?')
                params.append(f'%{val or v}%')
            else:
                clauses.append(f'{k} = ?')
                params.append(v)
        if 'q' in filters and model_name in self.models:
            q_val = filters['q']
            fields = self.models[model_name]['fields']
            text_fields = [f for f, data in fields.items() if data['type'] == 'text']
            if text_fields:
                q_clauses = ' OR '.join([f'{f} LIKE ?' for f in text_fields])
                if clauses:
                    clauses = [f"({' AND '.join(clauses)}) AND ({q_clauses})"]
                else:
                    clauses = [q_clauses]
                params.extend([f'%{q_val}%'] * len(text_fields))
        if not clauses:
            return ('', [])
        return (' WHERE ' + ' AND '.join(clauses), params)

    def insert(self, model_name: str, data: dict):
        table = self.models[model_name]['table']
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *'
        res = self.execute_query(query, tuple(data.values()))
        return res[0] if res else None

    def find(self, model_name: str, filters: dict=None):
        table = self.models[model_name]['table']
        where_clause, params = self._build_where(model_name, filters)
        query = f'SELECT * FROM {table}{where_clause}'
        if filters:
            sort = filters.get('sort')
            order = filters.get('order', 'asc')
            if sort:
                if sort.startswith('-'):
                    sort = sort[1:]
                    order = 'desc'
                query += f' ORDER BY {sort} {order}'
            limit = filters.get('limit', 20)
            offset = filters.get('offset', (int(filters.get('page', 1)) - 1) * int(limit))
            query += f' LIMIT {int(limit)} OFFSET {int(offset)}'
        return self.execute_query(query, tuple(params))

    def find_one(self, model_name: str, id: int):
        table = self.models[model_name]['table']
        res = self.execute_query(f'SELECT * FROM {table} WHERE id = ?', (id,))
        return res[0] if res else None

    def update(self, model_name: str, id: int, data: dict):
        table = self.models[model_name]['table']
        set_clauses = ', '.join([f'{k} = ?' for k in data.keys()])
        query = f'UPDATE {table} SET {set_clauses}, updated_at = CURRENT_TIMESTAMP WHERE id = ? RETURNING *'
        params = list(data.values()) + [id]
        res = self.execute_query(query, tuple(params))
        return res[0] if res else None

    def delete(self, model_name: str, id: int):
        table = self.models[model_name]['table']
        self.execute_query(f'DELETE FROM {table} WHERE id = ?', (id,))
        return True

    def count(self, model_name: str, filters: dict=None):
        table = self.models[model_name]['table']
        where_clause, params = self._build_where(model_name, filters)
        res = self.execute_query(f'SELECT COUNT(*) as c FROM {table}{where_clause}', tuple(params))
        return res[0]['c'] if res else 0

    def exists(self, model_name: str, id: int):
        table = self.models[model_name]['table']
        res = self.execute_query(f'SELECT 1 FROM {table} WHERE id = ?', (id,))
        return len(res) > 0
