from typing import List, Optional
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models import AuditLog
from models import ProductOrder
from schemas import ProductOrderCreate, ProductOrderUpdate, ProductOrderResponse, PaginatedProductOrderResponse
from logger import get_logger
from event_bus import event_bus, Event

router = APIRouter(prefix='/product_order', tags=['product_order'])
logger = get_logger(__name__)

@router.get('/', response_model=PaginatedProductOrderResponse)
def read_product_order_list(request: Request, page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db)):
    from sqlalchemy import or_, func
    query = db.query(ProductOrder)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=ProductOrderResponse)
def read_product_order(request: Request, item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(ProductOrder).filter(ProductOrder.product_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=ProductOrderResponse)
def create_product_order(request: Request, background_tasks: BackgroundTasks, item: ProductOrderCreate, db: Session = Depends(get_db)):
    db_item = ProductOrder(**item.model_dump())
    db.add(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='create', entity_name='product_order', entity_id=getattr(db_item, 'product_id', ''), request_id=req_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Created product_order {getattr(db_item, "product_id", "")}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'product_order', 'action': 'create'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='product_order.created', entity='product_order', action='create', payload={'id': getattr(db_item, 'product_id', ''), 'data': item.model_dump()}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.put('/{item_id}', response_model=ProductOrderResponse)
def update_product_order(request: Request, background_tasks: BackgroundTasks, item_id: str, item: ProductOrderUpdate, db: Session = Depends(get_db)):
    db_item = db.query(ProductOrder).filter(ProductOrder.product_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='update', entity_name='product_order', entity_id=item_id, request_id=req_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Updated product_order {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'product_order', 'action': 'update'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='product_order.updated', entity='product_order', action='update', payload={'id': item_id, 'data': update_data}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.delete('/{item_id}', response_model=ProductOrderResponse)
def delete_product_order(request: Request, background_tasks: BackgroundTasks, item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(ProductOrder).filter(ProductOrder.product_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='delete', entity_name='product_order', entity_id=item_id, request_id=req_id))
    db.commit()
    logger.info(f'Deleted product_order {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'product_order', 'action': 'delete'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='product_order.deleted', entity='product_order', action='delete', payload={'id': item_id}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item
