from typing import List, Optional
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from database import get_db
from models import AuditLog
from models import Permission
from schemas import PermissionCreate, PermissionUpdate, PermissionResponse, PaginatedPermissionResponse
from logger import get_logger
from auth import require_permission

router = APIRouter(prefix='/permission', tags=['permission'])
logger = get_logger(__name__)

@router.get('/', response_model=PaginatedPermissionResponse)
def read_permission_list(request: Request, page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    from sqlalchemy import or_, func
    query = db.query(Permission)
    if search:
        query = query.filter(or_(or_(Permission.name.ilike(f'%{search}%'), func.lower(Permission.name).contains(search.lower()))))
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=PermissionResponse)
def read_permission(request: Request, item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    db_item = db.query(Permission).filter(Permission.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=PermissionResponse)
def create_permission(request: Request, item: PermissionCreate, db: Session = Depends(get_db), _=Depends(require_permission('create'))):
    if getattr(item, 'name', None):
        existing = db.query(Permission).filter(Permission.name == item.name).first()
        if existing:
            raise HTTPException(status_code=400, detail='name already in use')
    db_item = Permission(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='create', entity_name='permission', entity_id=getattr(db_item, 'id', ''), request_id=req_id, user_id=usr_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Created permission {getattr(db_item, "id", "")}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'permission', 'action': 'create'})
    return db_item

@router.put('/{item_id}', response_model=PermissionResponse)
def update_permission(request: Request, item_id: str, item: PermissionUpdate, db: Session = Depends(get_db), _=Depends(require_permission('update'))):
    db_item = db.query(Permission).filter(Permission.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='update', entity_name='permission', entity_id=item_id, request_id=req_id, user_id=usr_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Updated permission {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'permission', 'action': 'update'})
    return db_item

@router.delete('/{item_id}', response_model=PermissionResponse)
def delete_permission(request: Request, item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('delete'))):
    db_item = db.query(Permission).filter(Permission.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='delete', entity_name='permission', entity_id=item_id, request_id=req_id, user_id=usr_id))
    db.commit()
    logger.info(f'Deleted permission {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'permission', 'action': 'delete'})
    return db_item
