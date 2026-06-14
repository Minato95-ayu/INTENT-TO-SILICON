from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserUpdate, UserResponse, PaginatedUserResponse

router = APIRouter(prefix='/user', tags=['user'])

@router.get('/', response_model=PaginatedUserResponse)
def read_user_list(page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db)):
    from sqlalchemy import or_, func
    query = db.query(User)
    if search:
        query = query.filter(or_(or_(User.email.ilike(f'%{search}%'), func.lower(User.email).contains(search.lower()))))
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=UserResponse)
def read_user(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(User).filter(User.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=UserResponse)
def create_user(item: UserCreate, db: Session = Depends(get_db)):
    if getattr(item, 'email', None):
        existing = db.query(User).filter(User.email == item.email).first()
        if existing:
            raise HTTPException(status_code=400, detail='email already in use')
    db_item = User(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/{item_id}', response_model=UserResponse)
def update_user(item_id: str, item: UserUpdate, db: Session = Depends(get_db)):
    db_item = db.query(User).filter(User.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/{item_id}', response_model=UserResponse)
def delete_user(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(User).filter(User.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    db.commit()
    return db_item
