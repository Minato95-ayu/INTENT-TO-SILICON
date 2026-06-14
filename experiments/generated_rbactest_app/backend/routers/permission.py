from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Permission
from schemas import PermissionCreate, PermissionUpdate, PermissionResponse, PaginatedPermissionResponse
from auth import require_permission

router = APIRouter(prefix='/permission', tags=['permission'])

@router.get('/', response_model=PaginatedPermissionResponse)
def read_permission_list(page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    from sqlalchemy import or_, func
    query = db.query(Permission)
    if search:
        query = query.filter(or_(or_(Permission.name.ilike(f'%{search}%'), func.lower(Permission.name).contains(search.lower()))))
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=PermissionResponse)
def read_permission(item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    db_item = db.query(Permission).filter(Permission.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=PermissionResponse)
def create_permission(item: PermissionCreate, db: Session = Depends(get_db), _=Depends(require_permission('create'))):
    if getattr(item, 'name', None):
        existing = db.query(Permission).filter(Permission.name == item.name).first()
        if existing:
            raise HTTPException(status_code=400, detail='name already in use')
    db_item = Permission(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/{item_id}', response_model=PermissionResponse)
def update_permission(item_id: str, item: PermissionUpdate, db: Session = Depends(get_db), _=Depends(require_permission('update'))):
    db_item = db.query(Permission).filter(Permission.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/{item_id}', response_model=PermissionResponse)
def delete_permission(item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('delete'))):
    db_item = db.query(Permission).filter(Permission.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    db.commit()
    return db_item
