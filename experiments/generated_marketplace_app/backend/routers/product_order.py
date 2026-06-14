from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import ProductOrder
from schemas import ProductOrderCreate, ProductOrderUpdate, ProductOrderResponse, PaginatedProductOrderResponse

router = APIRouter(prefix='/product_order', tags=['product_order'])

@router.get('/', response_model=PaginatedProductOrderResponse)
def read_product_order_list(page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db)):
    from sqlalchemy import or_, func
    query = db.query(ProductOrder)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=ProductOrderResponse)
def read_product_order(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(ProductOrder).filter(ProductOrder.product_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=ProductOrderResponse)
def create_product_order(item: ProductOrderCreate, db: Session = Depends(get_db)):
    db_item = ProductOrder(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put('/{item_id}', response_model=ProductOrderResponse)
def update_product_order(item_id: str, item: ProductOrderUpdate, db: Session = Depends(get_db)):
    db_item = db.query(ProductOrder).filter(ProductOrder.product_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/{item_id}', response_model=ProductOrderResponse)
def delete_product_order(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(ProductOrder).filter(ProductOrder.product_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    db.commit()
    return db_item
