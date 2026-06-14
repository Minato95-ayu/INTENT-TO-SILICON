from typing import List, Optional
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from database import get_db
from models import AuditLog
from models import StudentCourse
from schemas import StudentCourseCreate, StudentCourseUpdate, StudentCourseResponse, PaginatedStudentCourseResponse
from logger import get_logger

router = APIRouter(prefix='/student_course', tags=['student_course'])
logger = get_logger(__name__)

@router.get('/', response_model=PaginatedStudentCourseResponse)
def read_student_course_list(request: Request, page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db)):
    from sqlalchemy import or_, func
    query = db.query(StudentCourse)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=StudentCourseResponse)
def read_student_course(request: Request, item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(StudentCourse).filter(StudentCourse.student_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=StudentCourseResponse)
def create_student_course(request: Request, item: StudentCourseCreate, db: Session = Depends(get_db)):
    db_item = StudentCourse(**item.model_dump())
    db.add(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='create', entity_name='student_course', entity_id=getattr(db_item, 'student_id', ''), request_id=req_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Created student_course {getattr(db_item, "student_id", "")}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'student_course', 'action': 'create'})
    return db_item

@router.put('/{item_id}', response_model=StudentCourseResponse)
def update_student_course(request: Request, item_id: str, item: StudentCourseUpdate, db: Session = Depends(get_db)):
    db_item = db.query(StudentCourse).filter(StudentCourse.student_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='update', entity_name='student_course', entity_id=item_id, request_id=req_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Updated student_course {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'student_course', 'action': 'update'})
    return db_item

@router.delete('/{item_id}', response_model=StudentCourseResponse)
def delete_student_course(request: Request, item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(StudentCourse).filter(StudentCourse.student_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='delete', entity_name='student_course', entity_id=item_id, request_id=req_id))
    db.commit()
    logger.info(f'Deleted student_course {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'student_course', 'action': 'delete'})
    return db_item
