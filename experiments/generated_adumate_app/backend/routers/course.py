from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Course
from ..schemas import CourseCreate, CourseUpdate, CourseResponse

router = APIRouter(prefix='/course', tags=['course'])

@router.get('/', response_model=List[CourseResponse])
def read_course_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Course).offset(skip).limit(limit).all()

@router.get('/{item_id}', response_model=CourseResponse)
def read_course(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Course).filter(Course.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=CourseResponse)
def create_course(item: CourseCreate, db: Session = Depends(get_db)):
    db_item = Course(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/{item_id}', response_model=CourseResponse)
def update_course(item_id: str, item: CourseUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Course).filter(Course.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/{item_id}', response_model=CourseResponse)
def delete_course(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Course).filter(Course.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    db.commit()
    return db_item
