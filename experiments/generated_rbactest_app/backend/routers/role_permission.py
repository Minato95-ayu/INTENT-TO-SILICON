"""
=============================================================================
FILE: role_permission.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from typing import List, Optional
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models import AuditLog
from models import RolePermission
from schemas import RolePermissionCreate, RolePermissionUpdate, RolePermissionResponse, PaginatedRolePermissionResponse
from logger import get_logger
from auth import require_permission
from event_bus import event_bus, Event

router = APIRouter(prefix='/role_permission', tags=['role_permission'])
logger = get_logger(__name__)

@router.get('/', response_model=PaginatedRolePermissionResponse)
def read_role_permission_list(request: Request, page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    from sqlalchemy import or_, func
    query = db.query(RolePermission)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=RolePermissionResponse)
def read_role_permission(request: Request, item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    db_item = db.query(RolePermission).filter(RolePermission.role_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=RolePermissionResponse)
def create_role_permission(request: Request, background_tasks: BackgroundTasks, item: RolePermissionCreate, db: Session = Depends(get_db), _=Depends(require_permission('create'))):
    db_item = RolePermission(**item.model_dump())
    db.add(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='create', entity_name='role_permission', entity_id=getattr(db_item, 'role_id', ''), request_id=req_id, user_id=usr_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Created role_permission {getattr(db_item, "role_id", "")}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'role_permission', 'action': 'create'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='role_permission.created', entity='role_permission', action='create', payload={'id': getattr(db_item, 'role_id', ''), 'data': item.model_dump()}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.put('/{item_id}', response_model=RolePermissionResponse)
def update_role_permission(request: Request, background_tasks: BackgroundTasks, item_id: str, item: RolePermissionUpdate, db: Session = Depends(get_db), _=Depends(require_permission('update'))):
    db_item = db.query(RolePermission).filter(RolePermission.role_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='update', entity_name='role_permission', entity_id=item_id, request_id=req_id, user_id=usr_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Updated role_permission {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'role_permission', 'action': 'update'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='role_permission.updated', entity='role_permission', action='update', payload={'id': item_id, 'data': update_data}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.delete('/{item_id}', response_model=RolePermissionResponse)
def delete_role_permission(request: Request, background_tasks: BackgroundTasks, item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('delete'))):
    db_item = db.query(RolePermission).filter(RolePermission.role_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='delete', entity_name='role_permission', entity_id=item_id, request_id=req_id, user_id=usr_id))
    db.commit()
    logger.info(f'Deleted role_permission {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'role_permission', 'action': 'delete'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='role_permission.deleted', entity='role_permission', action='delete', payload={'id': item_id}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item
