from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Product
from schemas import ProductCreate, ProductUpdate, ProductResponse, PaginatedProductResponse

router = APIRouter(prefix='/product', tags=['product'])

@router.get('/', response_model=PaginatedProductResponse)
def read_product_list(page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db)):
    from sqlalchemy import or_, func
    query = db.query(Product)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=ProductResponse)
def read_product(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Product).filter(Product.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=ProductResponse)
def create_product(item: ProductCreate, db: Session = Depends(get_db)):
    db_item = Product(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/{item_id}', response_model=ProductResponse)
def update_product(item_id: str, item: ProductUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Product).filter(Product.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/{item_id}', response_model=ProductResponse)
def delete_product(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Product).filter(Product.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    db.commit()
    return db_item
