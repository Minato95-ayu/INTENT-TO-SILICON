from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import UserRole
from schemas import UserRoleCreate, UserRoleUpdate, UserRoleResponse, PaginatedUserRoleResponse
from auth import require_permission

router = APIRouter(prefix='/user_role', tags=['user_role'])

@router.get('/', response_model=PaginatedUserRoleResponse)
def read_user_role_list(page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    from sqlalchemy import or_, func
    query = db.query(UserRole)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=UserRoleResponse)
def read_user_role(item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('read'))):
    db_item = db.query(UserRole).filter(UserRole.user_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=UserRoleResponse)
def create_user_role(item: UserRoleCreate, db: Session = Depends(get_db), _=Depends(require_permission('create'))):
    db_item = UserRole(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/{item_id}', response_model=UserRoleResponse)
def update_user_role(item_id: str, item: UserRoleUpdate, db: Session = Depends(get_db), _=Depends(require_permission('update'))):
    db_item = db.query(UserRole).filter(UserRole.user_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/{item_id}', response_model=UserRoleResponse)
def delete_user_role(item_id: str, db: Session = Depends(get_db), _=Depends(require_permission('delete'))):
    db_item = db.query(UserRole).filter(UserRole.user_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    db.commit()
    return db_item
