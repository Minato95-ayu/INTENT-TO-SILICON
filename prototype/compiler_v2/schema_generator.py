"""
Aayu Schema Generator (Sprint 26)

Converts the pure semantic IRModel into a generic SchemaModel.
Handles standard database normalizations like foreign keys and junction tables.
"""

from .ir_nodes import IRModel
from .schema_nodes import SchemaModel, Table, Column

class SchemaGenerator:
    def __init__(self):
        pass

    def generate(self, ir_model: IRModel) -> SchemaModel:
        """
        Deterministically maps an IRModel to a database-agnostic SchemaModel.
        """
        schema = SchemaModel()
        
        # 1. Base Tables (Entities)
        for entity in ir_model.entities:
            # We already deduplicated entities in IRGenerator, so we just create tables safely
            # If IR somehow had duplicates, we could check here, but IR guarantees uniqueness
            if not schema.get_table(entity.name):
                t = Table(name=entity.name)
                # Every table gets a UUID primary key
                t.columns.append(Column(
                    name="id",
                    type="UUID",
                    is_primary_key=True
                ))
                schema.tables.append(t)

        # 2. Relationships (Foreign Keys & Junction Tables)
        for rel in ir_model.relationships:
            source_table = schema.get_table(rel.source)
            target_table = schema.get_table(rel.target)
            
            # Semantic Analyzer guarantees these exist, but just in case
            if not source_table or not target_table:
                continue
                
            cardinality = rel.cardinality
            
            if cardinality == "one_to_many":
                # Foreign key goes on the target (e.g., patient -> appointment => appointment.patient_id)
                fk_col = f"{rel.source}_id"
                # Prevent duplicate columns if relationship declared multiple times
                if not any(c.name == fk_col for c in target_table.columns):
                    target_table.columns.append(Column(
                        name=fk_col,
                        type="UUID",
                        is_foreign_key=True,
                        references_table=rel.source
                    ))
                    
            elif cardinality == "one_to_one":
                # Foreign key goes on the target, but must be UNIQUE
                fk_col = f"{rel.source}_id"
                if not any(c.name == fk_col for c in target_table.columns):
                    target_table.columns.append(Column(
                        name=fk_col,
                        type="UUID",
                        is_foreign_key=True,
                        references_table=rel.source,
                        is_unique=True
                    ))
                    
            elif cardinality == "many_to_many":
                # Create a junction table (e.g., student_course)
                junction_name = f"{rel.source}_{rel.target}"
                
                # Check if junction table already exists
                if not schema.get_table(junction_name):
                    junction_table = Table(name=junction_name)
                    
                    # Add FK back to source
                    junction_table.columns.append(Column(
                        name=f"{rel.source}_id",
                        type="UUID",
                        is_foreign_key=True,
                        references_table=rel.source
                    ))
                    
                    # Add FK back to target
                    junction_table.columns.append(Column(
                        name=f"{rel.target}_id",
                        type="UUID",
                        is_foreign_key=True,
                        references_table=rel.target
                    ))
                    
                    schema.tables.append(junction_table)
                    
            else:
                # Untyped relationship: Default to one_to_many as the most common architectural pattern
                fk_col = f"{rel.source}_id"
                if not any(c.name == fk_col for c in target_table.columns):
                    target_table.columns.append(Column(
                        name=fk_col,
                        type="UUID",
                        is_foreign_key=True,
                        references_table=rel.source
                    ))

        return schema
