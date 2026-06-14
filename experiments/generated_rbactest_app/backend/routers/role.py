from typing import List, Optional
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from database import get_db
from models import AuditLog
from models import Role
from schemas import RoleCreate, RoleUpdate, RoleResponse, PaginatedRoleResponse
from logger import get_logger
from auth import require_permission

router = APIRouter(prefix='/role', tags=['role'])
logger = get_logger(__name__)

@router.get('/', response_model=PaginatedRoleResponse)
def read_role_list(request: Request, page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    from sqlalchemy import or_, func
    query = db.query(Role)
    if search:
        query = query.filter(or_(or_(Role.name.ilike(f'%{search}%'), func.lower(Role.name).contains(search.lower()))))
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=RoleResponse)
def read_role(request: Request, item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    db_item = db.query(Role).filter(Role.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=RoleResponse)
def create_role(request: Request, item: RoleCreate, db: Session = Depends(get_db), _=Depends(require_permission('create'))):
    if getattr(item, 'name', None):
        existing = db.query(Role).filter(Role.name == item.name).first()
        if existing:
            raise HTTPException(status_code=400, detail='name already in use')
    db_item = Role(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='create', entity_name='role', entity_id=getattr(db_item, 'id', ''), request_id=req_id, user_id=usr_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Created role {getattr(db_item, "id", "")}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'role', 'action': 'create'})
    return db_item

@router.put('/{item_id}', response_model=RoleResponse)
def update_role(request: Request, item_id: str, item: RoleUpdate, db: Session = Depends(get_db), _=Depends(require_permission('update'))):
    db_item = db.query(Role).filter(Role.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='update', entity_name='role', entity_id=item_id, request_id=req_id, user_id=usr_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Updated role {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'role', 'action': 'update'})
    return db_item

@router.delete('/{item_id}', response_model=RoleResponse)
def delete_role(request: Request, item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('delete'))):
    db_item = db.query(Role).filter(Role.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='delete', entity_name='role', entity_id=item_id, request_id=req_id, user_id=usr_id))
    db.commit()
    logger.info(f'Deleted role {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'role', 'action': 'delete'})
    return db_item
