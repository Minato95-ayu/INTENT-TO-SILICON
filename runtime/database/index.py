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
AAYU Runtime — Index Engine
Automatically generates database indexes for foreign keys,
unique fields, and frequently queried columns.
"""


class IndexEngine:
    """
    Automatic index generation for the AAYU database subsystem.

    Features:
    - Auto-index foreign key columns for JOIN performance
    - Auto-index @unique decorated fields
    - Support for composite indexes via model decorators
    - Index existence checking to prevent duplicates
    """

    def get_indices(self, schema_ir):
        """
        Analyze schema IR and return a list of indexes to create.

        Args:
            schema_ir: Dict of {table_name: {field_name: field_meta, ...}}

        Returns:
            list[dict]: Each dict describes an index to create:
                {"table": str, "columns": list[str], "unique": bool, "name": str}
        """
        indices = []

        for table_name, fields in schema_ir.items():
            for field_name, field_meta in fields.items():
                if not isinstance(field_meta, dict):
                    continue

                # Auto-index foreign key columns
                if field_meta.get("foreign_key") or field_name.endswith("_id"):
                    index_name = f"idx_{table_name}_{field_name}"
                    indices.append({
                        "table": table_name,
                        "columns": [field_name],
                        "unique": False,
                        "name": index_name,
                    })

                # Auto-index @unique fields
                if field_meta.get("unique"):
                    index_name = f"idx_{table_name}_{field_name}_unique"
                    indices.append({
                        "table": table_name,
                        "columns": [field_name],
                        "unique": True,
                        "name": index_name,
                    })

                # Auto-index email fields (commonly queried)
                if field_meta.get("type") == "Email":
                    index_name = f"idx_{table_name}_{field_name}"
                    indices.append({
                        "table": table_name,
                        "columns": [field_name],
                        "unique": True,
                        "name": index_name,
                    })

        return indices

    def apply_indices(self, indices, adapter):
        """
        Create the given indexes on the database.

        Safely handles the case where an index already exists
        by using CREATE INDEX IF NOT EXISTS.

        Args:
            indices: List of index definitions from get_indices().
            adapter: Database adapter with execute_raw() method.
        """
        for idx in indices:
            unique_clause = "UNIQUE " if idx["unique"] else ""
            columns = ", ".join(idx["columns"])
            sql = (
                f"CREATE {unique_clause}INDEX IF NOT EXISTS "
                f"{idx['name']} ON {idx['table']} ({columns});"
            )
            try:
                adapter.execute_raw(sql)
                print(f"[Index] Created: {idx['name']} on {idx['table']}({columns})")
            except Exception as e:
                # Log but don't fail — indexes are performance optimization, not critical
                print(f"[Index] Warning: Failed to create {idx['name']}: {e}")
