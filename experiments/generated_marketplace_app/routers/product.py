from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Product
from ..schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix='/product', tags=['product'])

@router.get('/', response_model=List[ProductResponse])
def read_product_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()

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
