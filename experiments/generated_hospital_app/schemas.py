from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class PatientCreate(BaseModel):
    pass

class PatientUpdate(BaseModel):
    pass

class PatientResponse(PatientCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class DoctorCreate(BaseModel):
    pass

class DoctorUpdate(BaseModel):
    pass

class DoctorResponse(DoctorCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str

class AppointmentUpdate(BaseModel):
    patient_id: Optional[str] = None
    doctor_id: Optional[str] = None

class AppointmentResponse(AppointmentCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)
