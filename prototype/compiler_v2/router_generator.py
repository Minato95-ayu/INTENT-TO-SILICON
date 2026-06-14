"""
Aayu Router Generator

Generates individual FastAPI router files for each schema table.
"""
from typing import Dict
from .schema_nodes import SchemaModel, Table

class RouterGenerator:
    def _to_pascal_case(self, snake_str: str) -> str:
        components = snake_str.split('_')
        return "".join(x.title() for x in components)

    def generate(self, schema: SchemaModel) -> Dict[str, str]:
        routers = {}
        for table in schema.tables:
            route_name = table.name
            pascal_name = self._to_pascal_case(table.name)
            
            lines = [
                "from typing import List",
                "import uuid",
                "from fastapi import APIRouter, Depends, HTTPException",
                "from sqlalchemy.orm import Session",
                "from ..database import get_db",
                f"from ..models import {pascal_name}",
                f"from ..schemas import {pascal_name}Create, {pascal_name}Update, {pascal_name}Response",
                "",
                f"router = APIRouter(prefix='/{route_name}', tags=['{route_name}'])",
                ""
            ]
            
            # GET List
            lines.append(f"@router.get('/', response_model=List[{pascal_name}Response])")
            lines.append(f"def read_{route_name}_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):")
            lines.append(f"    return db.query({pascal_name}).offset(skip).limit(limit).all()\n")
            
            # GET Item
            lines.append(f"@router.get('/{{item_id}}', response_model={pascal_name}Response)")
            lines.append(f"def read_{route_name}(item_id: str, db: Session = Depends(get_db)):")
            lines.append(f"    db_item = db.query({pascal_name}).filter({pascal_name}.id == item_id).first()")
            lines.append(f"    if db_item is None:")
            lines.append(f"        raise HTTPException(status_code=404, detail='Not found')")
            lines.append(f"    return db_item\n")
            
            # POST
            lines.append(f"@router.post('/', response_model={pascal_name}Response)")
            lines.append(f"def create_{route_name}(item: {pascal_name}Create, db: Session = Depends(get_db)):")
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
            lines.append(f"@router.put('/{{item_id}}', response_model={pascal_name}Response)")
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
            lines.append(f"@router.delete('/{{item_id}}', response_model={pascal_name}Response)")
            lines.append(f"def delete_{route_name}(item_id: str, db: Session = Depends(get_db)):")
            lines.append(f"    db_item = db.query({pascal_name}).filter({pascal_name}.id == item_id).first()")
            lines.append(f"    if db_item is None:")
            lines.append(f"        raise HTTPException(status_code=404, detail='Not found')")
            lines.append(f"    db.delete(db_item)")
            lines.append(f"    db.commit()")
            lines.append(f"    return db_item\n")
            
            routers[f"{route_name}.py"] = "\n".join(lines)
            
        return routers
