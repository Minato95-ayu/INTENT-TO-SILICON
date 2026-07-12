class MigrationEngine:
    def apply(self, schema_ir, adapter):
        # Generates DDL and applies it
        for table, fields in schema_ir.items():
            adapter.create_table(table, fields)
