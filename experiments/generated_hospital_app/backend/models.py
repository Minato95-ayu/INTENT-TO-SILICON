from sqlalchemy import Column, String, Integer, ForeignKey
from .database import Base

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

