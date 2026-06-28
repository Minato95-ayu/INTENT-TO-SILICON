import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from .api import StorageAPI

class SQLiteDriver(StorageAPI):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def setup(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    type TEXT,
                    name TEXT,
                    data TEXT,
                    created_at TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edges (
                    id TEXT PRIMARY KEY,
                    from_node TEXT,
                    to_node TEXT,
                    relation TEXT,
                    weight REAL,
                    created_at TEXT
                )
            """)
            conn.commit()

    def add_node(self, node_id: str, node_type: str, name: str, data: Dict[str, Any]) -> None:
        created_at = datetime.utcnow().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO nodes (id, type, name, data, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (node_id, node_type, name, json.dumps(data), created_at))
            conn.commit()

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, type, name, data, created_at FROM nodes WHERE id = ?", (node_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "type": row[1],
                    "name": row[2],
                    "data": json.loads(row[3]) if row[3] else {},
                    "created_at": row[4]
                }
            return None

    def get_node_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, type, name, data, created_at FROM nodes WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "type": row[1],
                    "name": row[2],
                    "data": json.loads(row[3]) if row[3] else {},
                    "created_at": row[4]
                }
            return None

    def get_nodes_by_type(self, node_type: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, type, name, data, created_at FROM nodes WHERE type = ?", (node_type,))
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "type": row[1],
                    "name": row[2],
                    "data": json.loads(row[3]) if row[3] else {},
                    "created_at": row[4]
                }
                for row in rows
            ]

    def add_edge(self, edge_id: str, from_node: str, to_node: str, relation: str, weight: float = 1.0) -> None:
        created_at = datetime.utcnow().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO edges (id, from_node, to_node, relation, weight, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (edge_id, from_node, to_node, relation, weight, created_at))
            conn.commit()

    def get_edges(self, from_node: Optional[str] = None, to_node: Optional[str] = None, relation: Optional[str] = None) -> List[Dict[str, Any]]:
        query = "SELECT id, from_node, to_node, relation, weight, created_at FROM edges WHERE 1=1"
        params = []
        if from_node:
            query += " AND from_node = ?"
            params.append(from_node)
        if to_node:
            query += " AND to_node = ?"
            params.append(to_node)
        if relation:
            query += " AND relation = ?"
            params.append(relation)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "from_node": row[1],
                    "to_node": row[2],
                    "relation": row[3],
                    "weight": row[4],
                    "created_at": row[5]
                }
                for row in rows
            ]
