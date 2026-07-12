"""
=============================================================================
FILE: user.py
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
from models import User
from schemas import UserCreate, UserUpdate, UserResponse, PaginatedUserResponse
from logger import get_logger
from auth import require_permission
from event_bus import event_bus, Event

router = APIRouter(prefix='/user', tags=['user'])
logger = get_logger(__name__)

@router.get('/', response_model=PaginatedUserResponse)
def read_user_list(request: Request, page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    from sqlalchemy import or_, func
    query = db.query(User)
    if search:
        query = query.filter(or_(or_(User.email.ilike(f'%{search}%'), func.lower(User.email).contains(search.lower()))))
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=UserResponse)
def read_user(request: Request, item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    db_item = db.query(User).filter(User.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=UserResponse)
def create_user(request: Request, background_tasks: BackgroundTasks, item: UserCreate, db: Session = Depends(get_db), _=Depends(require_permission('create'))):
    if getattr(item, 'email', None):
        existing = db.query(User).filter(User.email == item.email).first()
        if existing:
            raise HTTPException(status_code=400, detail='email already in use')
    db_item = User(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='create', entity_name='user', entity_id=getattr(db_item, 'id', ''), request_id=req_id, user_id=usr_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Created user {getattr(db_item, "id", "")}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'user', 'action': 'create'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='user.created', entity='user', action='create', payload={'id': getattr(db_item, 'id', ''), 'data': item.model_dump()}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.put('/{item_id}', response_model=UserResponse)
def update_user(request: Request, background_tasks: BackgroundTasks, item_id: str, item: UserUpdate, db: Session = Depends(get_db), _=Depends(require_permission('update'))):
    db_item = db.query(User).filter(User.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='update', entity_name='user', entity_id=item_id, request_id=req_id, user_id=usr_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Updated user {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'user', 'action': 'update'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='user.updated', entity='user', action='update', payload={'id': item_id, 'data': update_data}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.delete('/{item_id}', response_model=UserResponse)
def delete_user(request: Request, background_tasks: BackgroundTasks, item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('delete'))):
    db_item = db.query(User).filter(User.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='delete', entity_name='user', entity_id=item_id, request_id=req_id, user_id=usr_id))
    db.commit()
    logger.info(f'Deleted user {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'user', 'action': 'delete'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='user.deleted', entity='user', action='delete', payload={'id': item_id}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item
