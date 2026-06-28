from fastapi import APIRouter
from typing import List
from app.models import Patient, Doctor

router = APIRouter()

@router.get('/patients', response_model=List[Patient])
def get_patients():
    return []

@router.get('/doctors', response_model=List[Doctor])
def get_doctors():
    return []


