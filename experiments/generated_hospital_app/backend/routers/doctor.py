from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Doctor
from schemas import DoctorCreate, DoctorUpdate, DoctorResponse, PaginatedDoctorResponse

router = APIRouter(prefix='/doctor', tags=['doctor'])

@router.get('/', response_model=PaginatedDoctorResponse)
def read_doctor_list(page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db)):
    from sqlalchemy import or_, func
    query = db.query(Doctor)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=DoctorResponse)
def read_doctor(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Doctor).filter(Doctor.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=DoctorResponse)
def create_doctor(item: DoctorCreate, db: Session = Depends(get_db)):
    db_item = Doctor(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/{item_id}', response_model=DoctorResponse)
def update_doctor(item_id: str, item: DoctorUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Doctor).filter(Doctor.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/{item_id}', response_model=DoctorResponse)
def delete_doctor(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Doctor).filter(Doctor.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    db.commit()
    return db_item
