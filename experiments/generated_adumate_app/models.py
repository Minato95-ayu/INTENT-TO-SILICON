from sqlalchemy import Column, String, Integer, ForeignKey
from .database import Base

class Course(Base):
    __tablename__ = "course"

    id = Column(String, primary_key=True)


class RoomAllocation(Base):
    __tablename__ = "room_allocation"

    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey("student.id"), unique=True)


class Student(Base):
    __tablename__ = "student"

    id = Column(String, primary_key=True)


class StudentCourse(Base):
    __tablename__ = "student_course"

    student_id = Column(String, ForeignKey("student.id"), primary_key=True)
    course_id = Column(String, ForeignKey("course.id"), primary_key=True)

