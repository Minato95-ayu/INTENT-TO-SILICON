"""
=============================================================================
FILE: schemas.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class CourseCreate(BaseModel):
    pass

class CourseUpdate(BaseModel):
    pass

class CourseResponse(CourseCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedCourseResponse(BaseModel):
    items: List[CourseResponse]
    total: int
    page: int
    size: int

class RoomAllocationCreate(BaseModel):
    student_id: str

class RoomAllocationUpdate(BaseModel):
    student_id: Optional[str] = None

class RoomAllocationResponse(RoomAllocationCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedRoomAllocationResponse(BaseModel):
    items: List[RoomAllocationResponse]
    total: int
    page: int
    size: int

class StudentCreate(BaseModel):
    pass

class StudentUpdate(BaseModel):
    pass

class StudentResponse(StudentCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedStudentResponse(BaseModel):
    items: List[StudentResponse]
    total: int
    page: int
    size: int

class AuditLogCreate(BaseModel):
    timestamp: str
    action: str
    entity_name: str
    entity_id: str
    request_id: str

class AuditLogUpdate(BaseModel):
    timestamp: Optional[str] = None
    action: Optional[str] = None
    entity_name: Optional[str] = None
    entity_id: Optional[str] = None
    request_id: Optional[str] = None

class AuditLogResponse(AuditLogCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedAuditLogResponse(BaseModel):
    items: List[AuditLogResponse]
    total: int
    page: int
    size: int

class StudentCourseCreate(BaseModel):
    student_id: str
    course_id: str

class StudentCourseUpdate(BaseModel):
    student_id: Optional[str] = None
    course_id: Optional[str] = None

class StudentCourseResponse(StudentCourseCreate):
    model_config = ConfigDict(from_attributes=True)

class PaginatedStudentCourseResponse(BaseModel):
    items: List[StudentCourseResponse]
    total: int
    page: int
    size: int
