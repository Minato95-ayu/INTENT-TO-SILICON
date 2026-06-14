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

class AppointmentCreate(BaseModel):
    patient_id: str

class AppointmentUpdate(BaseModel):
    patient_id: Optional[str] = None

class AppointmentResponse(AppointmentCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedAppointmentResponse(BaseModel):
    items: List[AppointmentResponse]
    total: int
    page: int
    size: int

class AuditLogCreate(BaseModel):
    timestamp: str
    action: str
    entity_name: str
    entity_id: str
    request_id: str
    user_id: str

class AuditLogUpdate(BaseModel):
    timestamp: Optional[str] = None
    action: Optional[str] = None
    entity_name: Optional[str] = None
    entity_id: Optional[str] = None
    request_id: Optional[str] = None
    user_id: Optional[str] = None

class AuditLogResponse(AuditLogCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedAuditLogResponse(BaseModel):
    items: List[AuditLogResponse]
    total: int
    page: int
    size: int

class UserCreate(BaseModel):
    email: str
    password_hash: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password_hash: Optional[str] = None

class UserResponse(UserCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedUserResponse(BaseModel):
    items: List[UserResponse]
    total: int
    page: int
    size: int

class RoleCreate(BaseModel):
    name: str

class RoleUpdate(BaseModel):
    name: Optional[str] = None

class RoleResponse(RoleCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedRoleResponse(BaseModel):
    items: List[RoleResponse]
    total: int
    page: int
    size: int

class PermissionCreate(BaseModel):
    name: str

class PermissionUpdate(BaseModel):
    name: Optional[str] = None

class PermissionResponse(PermissionCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedPermissionResponse(BaseModel):
    items: List[PermissionResponse]
    total: int
    page: int
    size: int

class UserRoleCreate(BaseModel):
    user_id: str
    role_id: str

class UserRoleUpdate(BaseModel):
    user_id: Optional[str] = None
    role_id: Optional[str] = None

class UserRoleResponse(UserRoleCreate):
    model_config = ConfigDict(from_attributes=True)

class PaginatedUserRoleResponse(BaseModel):
    items: List[UserRoleResponse]
    total: int
    page: int
    size: int

class RolePermissionCreate(BaseModel):
    role_id: str
    permission_id: str

class RolePermissionUpdate(BaseModel):
    role_id: Optional[str] = None
    permission_id: Optional[str] = None

class RolePermissionResponse(RolePermissionCreate):
    model_config = ConfigDict(from_attributes=True)

class PaginatedRolePermissionResponse(BaseModel):
    items: List[RolePermissionResponse]
    total: int
    page: int
    size: int
