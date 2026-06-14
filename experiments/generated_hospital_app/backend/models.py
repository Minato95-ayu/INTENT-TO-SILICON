from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class Patient(Base):
    __tablename__ = "patient"

    id = Column(String, primary_key=True)


class Doctor(Base):
    __tablename__ = "doctor"

    id = Column(String, primary_key=True)


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patient.id"))
    doctor_id = Column(String, ForeignKey("doctor.id"))


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(String, primary_key=True)
    timestamp = Column(String)
    action = Column(String)
    entity_name = Column(String)
    entity_id = Column(String)
    request_id = Column(String)

