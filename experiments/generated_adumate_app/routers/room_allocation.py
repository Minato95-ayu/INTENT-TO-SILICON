from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import RoomAllocation
from ..schemas import RoomAllocationCreate, RoomAllocationUpdate, RoomAllocationResponse

router = APIRouter(prefix='/room_allocation', tags=['room_allocation'])

@router.get('/', response_model=List[RoomAllocationResponse])
def read_room_allocation_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(RoomAllocation).offset(skip).limit(limit).all()

@router.get('/{item_id}', response_model=RoomAllocationResponse)
def read_room_allocation(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(RoomAllocation).filter(RoomAllocation.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=RoomAllocationResponse)
def create_room_allocation(item: RoomAllocationCreate, db: Session = Depends(get_db)):
    if getattr(item, 'student_id', None):
        existing = db.query(RoomAllocation).filter(RoomAllocation.student_id == item.student_id).first()
        if existing:
            raise HTTPException(status_code=400, detail='student_id already in use')
    db_item = RoomAllocation(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/{item_id}', response_model=RoomAllocationResponse)
def update_room_allocation(item_id: str, item: RoomAllocationUpdate, db: Session = Depends(get_db)):
    db_item = db.query(RoomAllocation).filter(RoomAllocation.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/{item_id}', response_model=RoomAllocationResponse)
def delete_room_allocation(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(RoomAllocation).filter(RoomAllocation.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    db.commit()
    return db_item
