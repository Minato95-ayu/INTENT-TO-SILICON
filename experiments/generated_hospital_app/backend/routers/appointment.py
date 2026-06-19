from typing import List, Optional
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models import AuditLog
from models import Appointment
from schemas import AppointmentCreate, AppointmentUpdate, AppointmentResponse, PaginatedAppointmentResponse
from logger import get_logger
from event_bus import event_bus, Event

router = APIRouter(prefix='/appointment', tags=['appointment'])
logger = get_logger(__name__)

@router.get('/', response_model=PaginatedAppointmentResponse)
def read_appointment_list(request: Request, page: int = 1, size: int = Query(20, ge=1, le=100), search: Optional[str] = None, sort: Optional[str] = None, order: Optional[str] = 'asc', db: Session = Depends(get_db)):
    from sqlalchemy import or_, func
    query = db.query(Appointment)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {'items': items, 'total': total, 'page': page, 'size': size}

@router.get('/{item_id}', response_model=AppointmentResponse)
def read_appointment(request: Request, item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Appointment).filter(Appointment.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    return db_item

@router.post('/', response_model=AppointmentResponse)
def create_appointment(request: Request, background_tasks: BackgroundTasks, item: AppointmentCreate, db: Session = Depends(get_db)):
    db_item = Appointment(id=str(uuid.uuid4()), **item.model_dump())
    db.add(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='create', entity_name='appointment', entity_id=getattr(db_item, 'id', ''), request_id=req_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Created appointment {getattr(db_item, "id", "")}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'appointment', 'action': 'create'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='appointment.created', entity='appointment', action='create', payload={'id': getattr(db_item, 'id', ''), 'data': item.model_dump()}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.put('/{item_id}', response_model=AppointmentResponse)
def update_appointment(request: Request, background_tasks: BackgroundTasks, item_id: str, item: AppointmentUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Appointment).filter(Appointment.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='update', entity_name='appointment', entity_id=item_id, request_id=req_id))
    db.commit()
    db.refresh(db_item)
    logger.info(f'Updated appointment {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'appointment', 'action': 'update'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='appointment.updated', entity='appointment', action='update', payload={'id': item_id, 'data': update_data}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item

@router.delete('/{item_id}', response_model=AppointmentResponse)
def delete_appointment(request: Request, background_tasks: BackgroundTasks, item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Appointment).filter(Appointment.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(db_item)
    req_id = getattr(request.state, 'request_id', 'unknown')
    db.add(AuditLog(id=str(uuid.uuid4()), timestamp=datetime.utcnow(), action='delete', entity_name='appointment', entity_id=item_id, request_id=req_id))
    db.commit()
    logger.info(f'Deleted appointment {item_id}', extra={'request_id': getattr(request.state, 'request_id', 'unknown'), 'entity': 'appointment', 'action': 'delete'})
    event_bus.emit(background_tasks, Event(id=str(uuid.uuid4()), name='appointment.deleted', entity='appointment', action='delete', payload={'id': item_id}, request_id=getattr(request.state, 'request_id', 'unknown'), timestamp=datetime.utcnow()))
    return db_item
