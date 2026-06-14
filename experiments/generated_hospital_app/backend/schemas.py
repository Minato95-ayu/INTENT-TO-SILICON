from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class PatientCreate(BaseModel):
    pass

class PatientUpdate(BaseModel):
    pass

class PatientResponse(PatientCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedPatientResponse(BaseModel):
    items: List[PatientResponse]
    total: int
    page: int
    size: int

class DoctorCreate(BaseModel):
    pass

class DoctorUpdate(BaseModel):
    pass

class DoctorResponse(DoctorCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedDoctorResponse(BaseModel):
    items: List[DoctorResponse]
    total: int
    page: int
    size: int

class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str

class AppointmentUpdate(BaseModel):
    patient_id: Optional[str] = None
    doctor_id: Optional[str] = None

class AppointmentResponse(AppointmentCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedAppointmentResponse(BaseModel):
    items: List[AppointmentResponse]
    total: int
    page: int
    size: int
