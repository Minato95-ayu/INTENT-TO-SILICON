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
                "from typing import List, Optional",
                "import uuid",
                "from fastapi import APIRouter, Depends, HTTPException, Query",
                "from sqlalchemy.orm import Session",
                "from database import get_db",
                f"from models import {pascal_name}",
                f"from schemas import {pascal_name}Create, {pascal_name}Update, {pascal_name}Response, Paginated{pascal_name}Response",
                "",
                f"router = APIRouter(prefix='/{route_name}', tags=['{route_name}'])",
                ""
            ]
            
            if getattr(schema, 'has_rbac', False):
                lines.insert(7, "from auth import require_permission")
                dep_read = ", _=Depends(require_permission('read'))"
                dep_create = ", _=Depends(require_permission('create'))"
                dep_update = ", _=Depends(require_permission('update'))"
                dep_delete = ", _=Depends(require_permission('delete'))"
            else:
                dep_read = ""
                dep_create = ""
                dep_update = ""
                dep_delete = ""
            
            # GET List
            lines.append(f"@router.get('/', response_model=Paginated{pascal_name}Response)")
            lines.append(f"def read_{route_name}_list(page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db){dep_read}):")
            lines.append(f"    from sqlalchemy import or_, func")
            lines.append(f"    query = db.query({pascal_name})")
            
            # Apply Search Filtering
            if table.searchable_columns:
                lines.append(f"    if search:")
                conditions = []
                for col in table.searchable_columns:
                    # Case insensitive search with fallback
                    conditions.append(f"or_({pascal_name}.{col.name}.ilike(f'%{{search}}%'), func.lower({pascal_name}.{col.name}).contains(search.lower()))")
                search_condition = f"or_({', '.join(conditions)})"
                lines.append(f"        query = query.filter({search_condition})")
                
            lines.append(f"    total = query.count()")
            lines.append(f"    items = query.offset((page - 1) * size).limit(size).all()")
            lines.append(f"    return {{'items': items, 'total': total, 'page': page, 'size': size}}\n")
            
            has_id = any(c.name == 'id' for c in table.columns)
            id_field = 'id' if has_id else table.columns[0].name

            # GET Item
            lines.append(f"@router.get('/{{item_id}}', response_model={pascal_name}Response)")
            lines.append(f"def read_{route_name}(item_id: str, db: Session = Depends(get_db){dep_read}):")
            lines.append(f"    db_item = db.query({pascal_name}).filter({pascal_name}.{id_field} == item_id).first()")
            lines.append(f"    if db_item is None:")
            lines.append(f"        raise HTTPException(status_code=404, detail='Not found')")
            lines.append(f"    return db_item\n")
            
            # POST
            lines.append(f"@router.post('/', response_model={pascal_name}Response)")
            lines.append(f"def create_{route_name}(item: {pascal_name}Create, db: Session = Depends(get_db){dep_create}):")
            for col in table.columns:
                if col.is_unique:
                    lines.append(f"    if getattr(item, '{col.name}', None):")
                    lines.append(f"        existing = db.query({pascal_name}).filter({pascal_name}.{col.name} == item.{col.name}).first()")
                    lines.append(f"        if existing:")
                    lines.append(f"            raise HTTPException(status_code=400, detail='{col.name} already in use')")
                    
            if has_id:
                lines.append(f"    db_item = {pascal_name}(id=str(uuid.uuid4()), **item.model_dump())")
            else:
                lines.append(f"    db_item = {pascal_name}(**item.model_dump())")
            lines.append(f"    db.add(db_item)")
            lines.append(f"    db.commit()")
            lines.append(f"    db.refresh(db_item)")
            lines.append(f"    return db_item\n")
            
            # PUT
            lines.append(f"@router.put('/{{item_id}}', response_model={pascal_name}Response)")
            lines.append(f"def update_{route_name}(item_id: str, item: {pascal_name}Update, db: Session = Depends(get_db){dep_update}):")
            lines.append(f"    db_item = db.query({pascal_name}).filter({pascal_name}.{id_field} == item_id).first()")
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
            lines.append(f"def delete_{route_name}(item_id: str, db: Session = Depends(get_db){dep_delete}):")
            lines.append(f"    db_item = db.query({pascal_name}).filter({pascal_name}.{id_field} == item_id).first()")
            lines.append(f"    if db_item is None:")
            lines.append(f"        raise HTTPException(status_code=404, detail='Not found')")
            lines.append(f"    db.delete(db_item)")
            lines.append(f"    db.commit()")
            lines.append(f"    return db_item\n")
            
            routers[f"{route_name}.py"] = "\n".join(lines)
            
        return routers
