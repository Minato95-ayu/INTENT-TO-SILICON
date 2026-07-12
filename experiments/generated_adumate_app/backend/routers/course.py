"""
=============================================================================
FILE: course.py
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
from models import Course
from schemas import CourseCreate, CourseUpdate, CourseResponse, PaginatedCourseResponse
from logger import get_logger
from event_bus import event_bus, Event

router = APIRouter(prefix='/course', tags=['course'])
logger = get_logger(__name__)

@router.get('/', response_model=PaginatedCourseResponse)
def read_course_list(request: Request, page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db)):
    from sqlalchemy import or_, func
    query = db.query(Course)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=CourseResponse)
def read_course(request: Request, item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Course).filter(Course.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=CourseResponse)
def create_course(request: Request, background_tasks: BackgroundTasks, item: CourseCreate, db: Session = Depends(get_db)):
    db_item = Course(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='create', entity_name='course', entity_id=getattr(db_item, 'id', ''), request_id=req_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Created course {getattr(db_item, "id", "")}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'course', 'action': 'create'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='course.created', entity='course', action='create', payload={'id': getattr(db_item, 'id', ''), 'data': item.model_dump()}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.put('/{item_id}', response_model=CourseResponse)
def update_course(request: Request, background_tasks: BackgroundTasks, item_id: str, item: CourseUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Course).filter(Course.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='update', entity_name='course', entity_id=item_id, request_id=req_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Updated course {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'course', 'action': 'update'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='course.updated', entity='course', action='update', payload={'id': item_id, 'data': update_data}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.delete('/{item_id}', response_model=CourseResponse)
def delete_course(request: Request, background_tasks: BackgroundTasks, item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Course).filter(Course.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='delete', entity_name='course', entity_id=item_id, request_id=req_id))
    db.commit()
    logger.info(f'Deleted course {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'course', 'action': 'delete'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='course.deleted', entity='course', action='delete', payload={'id': item_id}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item
