from typing import List, Optional
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models import AuditLog
from models import UserRole
from schemas import UserRoleCreate, UserRoleUpdate, UserRoleResponse, PaginatedUserRoleResponse
from logger import get_logger
from auth import require_permission
from event_bus import event_bus, Event

router = APIRouter(prefix='/user_role', tags=['user_role'])
logger = get_logger(__name__)

@router.get('/', response_model=PaginatedUserRoleResponse)
def read_user_role_list(request: Request, page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    from sqlalchemy import or_, func
    query = db.query(UserRole)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=UserRoleResponse)
def read_user_role(request: Request, item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    db_item = db.query(UserRole).filter(UserRole.user_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=UserRoleResponse)
def create_user_role(request: Request, background_tasks: BackgroundTasks, item: UserRoleCreate, db: Session = Depends(get_db), _=Depends(require_permission('create'))):
    db_item = UserRole(**item.model_dump())
    db.add(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='create', entity_name='user_role', entity_id=getattr(db_item, 'user_id', ''), request_id=req_id, user_id=usr_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Created user_role {getattr(db_item, "user_id", "")}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'user_role', 'action': 'create'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='user_role.created', entity='user_role', action='create', payload={'id': getattr(db_item, 'user_id', ''), 'data': item.model_dump()}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.put('/{item_id}', response_model=UserRoleResponse)
def update_user_role(request: Request, background_tasks: BackgroundTasks, item_id: str, item: UserRoleUpdate, db: Session = Depends(get_db), _=Depends(require_permission('update'))):
    db_item = db.query(UserRole).filter(UserRole.user_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='update', entity_name='user_role', entity_id=item_id, request_id=req_id, user_id=usr_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Updated user_role {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'user_role', 'action': 'update'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='user_role.updated', entity='user_role', action='update', payload={'id': item_id, 'data': update_data}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.delete('/{item_id}', response_model=UserRoleResponse)
def delete_user_role(request: Request, background_tasks: BackgroundTasks, item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('delete'))):
    db_item = db.query(UserRole).filter(UserRole.user_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    usr_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else getattr(getattr(request.state, 'user', None), 'id', None)
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='delete', entity_name='user_role', entity_id=item_id, request_id=req_id, user_id=usr_id))
    db.commit()
    logger.info(f'Deleted user_role {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'user_role', 'action': 'delete'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='user_role.deleted', entity='user_role', action='delete', payload={'id': item_id}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item
