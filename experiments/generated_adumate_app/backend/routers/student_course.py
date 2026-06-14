from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import StudentCourse
from ..schemas import StudentCourseCreate, StudentCourseUpdate, StudentCourseResponse

router = APIRouter(prefix='/student_course', tags=['student_course'])

@router.get('/', response_model=List[StudentCourseResponse])
def read_student_course_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(StudentCourse).offset(skip).limit(limit).all()

@router.get('/{item_id}', response_model=StudentCourseResponse)
def read_student_course(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(StudentCourse).filter(StudentCourse.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=StudentCourseResponse)
def create_student_course(item: StudentCourseCreate, db: Session = Depends(get_db)):
    db_item = StudentCourse(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/{item_id}', response_model=StudentCourseResponse)
def update_student_course(item_id: str, item: StudentCourseUpdate, db: Session = Depends(get_db)):
    db_item = db.query(StudentCourse).filter(StudentCourse.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/{item_id}', response_model=StudentCourseResponse)
def delete_student_course(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(StudentCourse).filter(StudentCourse.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    db.commit()
    return db_item
