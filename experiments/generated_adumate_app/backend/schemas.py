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
