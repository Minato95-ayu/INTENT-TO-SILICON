from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class Patient(Base):
    __tablename__ = "patient"

    id = Column(String, primary_key=True)


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient.id"))


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(String, primary_key=True)
    timestamp = Column(String)
    action = Column(String)
    entity_name = Column(String)
    entity_id = Column(String)
    request_id = Column(String)
    user_id = Column(String)


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)


class Role(Base):
    __tablename__ = "role"

    id = Column(String, primary_key=True)

