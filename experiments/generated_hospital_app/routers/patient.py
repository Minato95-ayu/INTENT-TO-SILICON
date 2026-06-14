from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Patient
from ..schemas import PatientCreate, PatientUpdate, PatientResponse

router = APIRouter(prefix='/patient', tags=['patient'])

@router.get('/', response_model=List[PatientResponse])
def read_patient_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Patient).offset(skip).limit(limit).all()

@router.get('/{item_id}', response_model=PatientResponse)
def read_patient(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Patient).filter(Patient.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=PatientResponse)
def create_patient(item: PatientCreate, db: Session = Depends(get_db)):
    db_item = Patient(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/{item_id}', response_model=PatientResponse)
def update_patient(item_id: str, item: PatientUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Patient).filter(Patient.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/{item_id}', response_model=PatientResponse)
def delete_patient(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Patient).filter(Patient.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    db.commit()
    return db_item
