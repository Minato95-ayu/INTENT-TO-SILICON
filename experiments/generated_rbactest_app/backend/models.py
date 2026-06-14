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
    name = Column(String, unique=True)


class Permission(Base):
    __tablename__ = "permission"

    id = Column(String, primary_key=True)
    name = Column(String, unique=True)


class UserRole(Base):
    __tablename__ = "user_role"

    user_id = Column(String, ForeignKey("user.id"), primary_key=True)
    role_id = Column(String, ForeignKey("role.id"), primary_key=True)


class RolePermission(Base):
    __tablename__ = "role_permission"

    role_id = Column(String, ForeignKey("role.id"), primary_key=True)
    permission_id = Column(String, ForeignKey("permission.id"), primary_key=True)

