"""
Aayu FastAPI CRUD Generator (Sprint 29)

Converts the generic database-agnostic SchemaModel into valid FastAPI Application code.
Generates Pydantic schemas (Create, Update, Response) and FastAPI Router endpoints (CRUD) for each table.
"""

from .schema_nodes import SchemaModel, Table, Column

class FastAPIGenerator:
    def __init__(self):
        pass

    def _to_pascal_case(self, snake_str: str) -> str:
        """Converts snake_case table name to PascalCase class name."""
        components = snake_str.split('_')
        return "".join(x.title() for x in components)
        
    def _map_pydantic_type(self, generic_type: str) -> str:
        """Maps generic schema types to Python/Pydantic types."""
        if generic_type.upper() == "UUID":
            return "str"
        elif generic_type.upper() == "INTEGER":
            return "int"
        return "str"

    def generate(self, schema: SchemaModel) -> str:
        """
        Generates a valid Python script containing FastAPI Application, Pydantic schemas, and CRUD routes.
        This string is meant to be appended after the SQLAlchemy ORM models generation.
        """
        lines = []
        
        # 1. Imports
        lines.append("from typing import List, Optional")
        lines.append("import uuid")
        lines.append("from fastapi import FastAPI, Depends, HTTPException")
        lines.append("from pydantic import BaseModel, ConfigDict")
        lines.append("from sqlalchemy.orm import Session")
        lines.append("from sqlalchemy import create_engine")
        lines.append("from sqlalchemy.orm import sessionmaker")
        lines.append("from sqlalchemy.pool import StaticPool")
        
        lines.append("\n# Database Dependency setup (Assuming SQLite memory for testing, can be replaced)")
        lines.append("engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)")
        lines.append("SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)")
        
        lines.append("\ndef get_db():")
        lines.append("    db = SessionLocal()")
        lines.append("    try:")
        lines.append("        yield db")
        lines.append("    finally:")
        lines.append("        db.close()\n")
        
        lines.append("app = FastAPI(title='Aayu Generated API')\n")
        
        # 2. Pydantic Schemas
        lines.append("# --- PYDANTIC SCHEMAS ---")
        for table in schema.tables:
            pascal_name = self._to_pascal_case(table.name)
            
            # Create Schema
            lines.append(f"class {pascal_name}Create(BaseModel):")
            has_create_fields = False
            for col in table.columns:
                if col.name != "id": # Exclude 'id' from creation
                    ptype = self._map_pydantic_type(col.type)
                    # For V1, making foreign keys required
                    lines.append(f"    {col.name}: {ptype}")
                    has_create_fields = True
            if not has_create_fields:
                lines.append("    pass")
            lines.append("")
                
            # Update Schema (all fields optional)
            lines.append(f"class {pascal_name}Update(BaseModel):")
            has_update_fields = False
            for col in table.columns:
                if col.name != "id":
                    ptype = self._map_pydantic_type(col.type)
                    lines.append(f"    {col.name}: Optional[{ptype}] = None")
                    has_update_fields = True
            if not has_update_fields:
                lines.append("    pass")
            lines.append("")
                
            # Response Schema
            lines.append(f"class {pascal_name}Response({pascal_name}Create):")
            id_col_type = next((self._map_pydantic_type(c.type) for c in table.columns if c.name == "id"), "str")
            lines.append(f"    id: {id_col_type}")
            lines.append("    model_config = ConfigDict(from_attributes=True)\n")

        # 3. FastAPI Endpoints
        lines.append("# --- FASTAPI ENDPOINTS ---")
        for table in schema.tables:
            route_name = table.name
            pascal_name = self._to_pascal_case(table.name)
            
            # GET List
            lines.append(f"@app.get('/{route_name}', response_model=List[{pascal_name}Response])")
            lines.append(f"def read_{route_name}_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):")
            lines.append(f"    return db.query({pascal_name}).offset(skip).limit(limit).all()\n")
            
            # GET Item
            lines.append(f"@app.get('/{route_name}/{{item_id}}', response_model={pascal_name}Response)")
            lines.append(f"def read_{route_name}(item_id: str, db: Session = Depends(get_db)):")
            lines.append(f"    db_item = db.query({pascal_name}).filter({pascal_name}.id == item_id).first()")
            lines.append(f"    if db_item is None:")
            lines.append(f"        raise HTTPException(status_code=404, detail='Not found')")
            lines.append(f"    return db_item\n")
            
            # POST
            lines.append(f"@app.post('/{route_name}', response_model={pascal_name}Response)")
            lines.append(f"def create_{route_name}(item: {pascal_name}Create, db: Session = Depends(get_db)):")
            lines.append(f"    # Basic unique constraint check for 1-to-1 relationships for V1")
            for col in table.columns:
                if col.is_unique:
                    lines.append(f"    if getattr(item, '{col.name}', None):")
                    lines.append(f"        existing = db.query({pascal_name}).filter({pascal_name}.{col.name} == item.{col.name}).first()")
                    lines.append(f"        if existing:")
                    lines.append(f"            raise HTTPException(status_code=400, detail='{col.name} already in use')")
                    
            lines.append(f"    db_item = {pascal_name}(id=str(uuid.uuid4()), **item.model_dump())")
            lines.append(f"    db.add(db_item)")
            lines.append(f"    db.commit()")
            lines.append(f"    db.refresh(db_item)")
            lines.append(f"    return db_item\n")
            
            # PUT
            lines.append(f"@app.put('/{route_name}/{{item_id}}', response_model={pascal_name}Response)")
            lines.append(f"def update_{route_name}(item_id: str, item: {pascal_name}Update, db: Session = Depends(get_db)):")
            lines.append(f"    db_item = db.query({pascal_name}).filter({pascal_name}.id == item_id).first()")
            lines.append(f"    if db_item is None:")
            lines.append(f"        raise HTTPException(status_code=404, detail='Not found')")
            lines.append(f"    update_data = item.model_dump(exclude_unset=True)")
            lines.append(f"    for key, value in update_data.items():")
            lines.append(f"        setattr(db_item, key, value)")
            lines.append(f"    db.commit()")
            lines.append(f"    db.refresh(db_item)")
            lines.append(f"    return db_item\n")
            
            # DELETE
            lines.append(f"@app.delete('/{route_name}/{{item_id}}', response_model={pascal_name}Response)")
            lines.append(f"def delete_{route_name}(item_id: str, db: Session = Depends(get_db)):")
            lines.append(f"    db_item = db.query({pascal_name}).filter({pascal_name}.id == item_id).first()")
            lines.append(f"    if db_item is None:")
            lines.append(f"        raise HTTPException(status_code=404, detail='Not found')")
            lines.append(f"    db.delete(db_item)")
            lines.append(f"    db.commit()")
            lines.append(f"    return db_item\n")
            
        return "\n".join(lines)
