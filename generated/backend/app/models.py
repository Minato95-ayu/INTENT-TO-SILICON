from pydantic import BaseModel
from typing import Optional, List

class Patient(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class Doctor(BaseModel):
    name: Optional[str] = None


