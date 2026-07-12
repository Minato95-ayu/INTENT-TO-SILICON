"""
=============================================================================
FILE: models.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

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


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(String, primary_key=True)
    timestamp = Column(String)
    action = Column(String)
    entity_name = Column(String)
    entity_id = Column(String)
    request_id = Column(String)


class StudentCourse(Base):
    __tablename__ = "student_course"

    student_id = Column(String, ForeignKey("student.id"), primary_key=True)
    course_id = Column(String, ForeignKey("course.id"), primary_key=True)

