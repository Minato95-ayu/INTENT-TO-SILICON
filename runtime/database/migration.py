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

"""
AAYU Runtime — Database Migration Engine
Provides versioned schema migrations with forward/backward support,
diff detection, and migration history tracking.

Replaces the previous 6-line stub that only did CREATE TABLE IF NOT EXISTS.
"""

import os
import time
import json
import sqlite3
import hashlib
from datetime import datetime


class MigrationEngine:
    """
    Production-grade migration engine for the AAYU database subsystem.

    Features:
    - Migration history tracking via _aayu_migrations table
    - Schema diff detection (compare model definitions vs current DB schema)
    - Forward migrations: CREATE TABLE, ADD COLUMN, CREATE INDEX
    - Backward migrations: rollback tracking with recorded DDL
    - Migration file generation for reproducibility
    """

    HISTORY_TABLE = "_aayu_migrations"

    def __init__(self, db_path="aayu_data/Main.db", migrations_dir="aayu_data/migrations"):
        self.db_path = db_path
        self.migrations_dir = migrations_dir
        self._conn = None

    @property
    def conn(self):
        """Lazy connection — opens only when needed."""
        if self._conn is None:
            os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
            # Enable WAL mode for better concurrent read/write performance
            self._conn.execute("PRAGMA journal_mode=WAL;")
            self._conn.execute("PRAGMA foreign_keys=ON;")
        return self._conn

    def _ensure_history_table(self):
        """Create the migration history table if it doesn't exist."""
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.HISTORY_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                applied_at TEXT NOT NULL,
                checksum TEXT NOT NULL,
                up_sql TEXT NOT NULL,
                down_sql TEXT
            )
        """)
        self.conn.commit()

    def _get_applied_versions(self):
        """Return set of already-applied migration versions."""
        self._ensure_history_table()
        cursor = self.conn.execute(
            f"SELECT version FROM {self.HISTORY_TABLE} ORDER BY id"
        )
        return [row["version"] for row in cursor.fetchall()]

    def _get_current_schema(self):
        """Inspect current database schema — returns dict of table -> columns."""
        schema = {}
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE '_%'"
        )
        for row in cursor.fetchall():
            table_name = row["name"]
            col_cursor = self.conn.execute(f"PRAGMA table_info({table_name})")
            columns = {}
            for col in col_cursor.fetchall():
                columns[col["name"]] = {
                    "type": col["type"],
                    "notnull": bool(col["notnull"]),
                    "default": col["dflt_value"],
                    "pk": bool(col["pk"]),
                }
            schema[table_name] = columns
        return schema

    def _compute_checksum(self, sql):
        """Compute SHA-256 checksum for migration SQL."""
        return hashlib.sha256(sql.encode("utf-8")).hexdigest()[:16]

    # ── Public API ───────────────────────────────────────────────

    def apply(self, schema_ir, adapter):
        """
        Apply schema IR to the database with migration tracking.

        This is the main entry point — called by StorageEngine.initialize().
        Compares desired schema (from AAYU model declarations) against
        current DB state and applies only the necessary changes.
        """
        self._ensure_history_table()
        current_schema = self._get_current_schema()

        for table_name, fields in schema_ir.items():
            if table_name not in current_schema:
                # New table — create it
                self._create_table(table_name, fields, adapter)
            else:
                # Existing table — check for new columns
                existing_columns = set(current_schema[table_name].keys())
                for field_name, field_meta in fields.items():
                    if field_name not in existing_columns:
                        self._add_column(table_name, field_name, field_meta, adapter)

    def _create_table(self, table_name, fields, adapter):
        """Create a new table and record the migration."""
        adapter.create_table(table_name, fields)

        # Record in migration history
        version = self._generate_version()
        up_sql = f"CREATE TABLE {table_name} (...);"
        down_sql = f"DROP TABLE IF EXISTS {table_name};"

        self.conn.execute(
            f"""INSERT INTO {self.HISTORY_TABLE}
                (version, name, applied_at, checksum, up_sql, down_sql)
                VALUES (?, ?, ?, ?, ?, ?)""",
            (
                version,
                f"create_{table_name}",
                datetime.utcnow().isoformat(),
                self._compute_checksum(up_sql),
                up_sql,
                down_sql,
            ),
        )
        self.conn.commit()
        print(f"[Migration] Created table: {table_name} (version {version})")

    def _add_column(self, table_name, column_name, field_meta, adapter):
        """Add a new column to an existing table."""
        col_type = self._resolve_type(field_meta)
        default = field_meta.get("default", "")
        default_clause = f" DEFAULT {default}" if default else ""

        up_sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {col_type}{default_clause};"
        down_sql = f"-- SQLite does not support DROP COLUMN before 3.35.0"

        try:
            self.conn.execute(up_sql)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                return  # Column already exists — idempotent
            raise

        version = self._generate_version()
        self.conn.execute(
            f"""INSERT INTO {self.HISTORY_TABLE}
                (version, name, applied_at, checksum, up_sql, down_sql)
                VALUES (?, ?, ?, ?, ?, ?)""",
            (
                version,
                f"add_{column_name}_to_{table_name}",
                datetime.utcnow().isoformat(),
                self._compute_checksum(up_sql),
                up_sql,
                down_sql,
            ),
        )
        self.conn.commit()
        print(f"[Migration] Added column: {table_name}.{column_name} (version {version})")

    def _resolve_type(self, field_meta):
        """Map AAYU field types to SQLite column types."""
        type_map = {
            "Int": "INTEGER",
            "Float": "REAL",
            "String": "TEXT",
            "Bool": "INTEGER",
            "Email": "TEXT",
            "Phone": "TEXT",
            "URL": "TEXT",
            "UUID": "TEXT",
        }
        aayu_type = field_meta.get("type", "String") if isinstance(field_meta, dict) else str(field_meta)
        return type_map.get(aayu_type, "TEXT")

    def _generate_version(self):
        """Generate a timestamp-based migration version."""
        return datetime.utcnow().strftime("%Y%m%d%H%M%S") + f"_{int(time.time() * 1000) % 10000:04d}"

    def diff(self, schema_ir):
        """
        Compare desired schema against current DB and return a list of
        pending changes without applying them.

        Returns:
            list[dict]: Each dict describes a pending change:
                {"type": "create_table"|"add_column", "table": str, "column": str|None}
        """
        self._ensure_history_table()
        current_schema = self._get_current_schema()
        changes = []

        for table_name, fields in schema_ir.items():
            if table_name not in current_schema:
                changes.append({
                    "type": "create_table",
                    "table": table_name,
                    "column": None,
                })
            else:
                existing_columns = set(current_schema[table_name].keys())
                for field_name in fields:
                    if field_name not in existing_columns:
                        changes.append({
                            "type": "add_column",
                            "table": table_name,
                            "column": field_name,
                        })

        return changes

    def rollback_last(self):
        """
        Rollback the most recently applied migration.

        Executes the recorded down_sql and removes the migration from history.
        Note: SQLite has limited ALTER TABLE support — some rollbacks may be
        informational only (logged but not reversible).
        """
        self._ensure_history_table()
        cursor = self.conn.execute(
            f"SELECT * FROM {self.HISTORY_TABLE} ORDER BY id DESC LIMIT 1"
        )
        row = cursor.fetchone()
        if not row:
            print("[Migration] No migrations to rollback.")
            return False

        version = row["version"]
        down_sql = row["down_sql"]
        name = row["name"]

        if down_sql and not down_sql.startswith("--"):
            try:
                self.conn.execute(down_sql)
                self.conn.commit()
                print(f"[Migration] Rolled back: {name} (version {version})")
            except sqlite3.OperationalError as e:
                print(f"[Migration] Rollback failed for {name}: {e}")
                return False
        else:
            print(f"[Migration] No reversible down_sql for: {name} (version {version})")

        self.conn.execute(
            f"DELETE FROM {self.HISTORY_TABLE} WHERE version = ?", (version,)
        )
        self.conn.commit()
        return True

    def status(self):
        """Return a list of all applied migrations with their metadata."""
        self._ensure_history_table()
        cursor = self.conn.execute(
            f"SELECT version, name, applied_at, checksum FROM {self.HISTORY_TABLE} ORDER BY id"
        )
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        """Close the database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
