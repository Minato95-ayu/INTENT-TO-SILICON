"""
=============================================================================
FILE: conftest.py
PURPOSE: Test file - Validates system functionality
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test file - validates system functionality.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import pytest
import sys
import os
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def admin_client(client, db_session):
    from models import User, Role, Permission, UserRole, RolePermission
    from auth import get_password_hash, create_access_token
    
    # Create permissions
    p_read = Permission(id=str(uuid.uuid4()), name='read')
    p_create = Permission(id=str(uuid.uuid4()), name='create')
    p_update = Permission(id=str(uuid.uuid4()), name='update')
    p_delete = Permission(id=str(uuid.uuid4()), name='delete')
    
    # Create admin role
    r_admin = Role(id=str(uuid.uuid4()), name='admin')
    
    # Create admin user
    u_admin = User(id=str(uuid.uuid4()), email='admin@test.com', password_hash=get_password_hash('adminpass'))
    
    db_session.add_all([p_read, p_create, p_update, p_delete, r_admin, u_admin])
    db_session.commit()
    
    # Link permission to role
    db_session.add_all([
        RolePermission(role_id=r_admin.id, permission_id=p_read.id),
        RolePermission(role_id=r_admin.id, permission_id=p_create.id),
        RolePermission(role_id=r_admin.id, permission_id=p_update.id),
        RolePermission(role_id=r_admin.id, permission_id=p_delete.id)
    ])
    
    # Link role to user
    db_session.add(UserRole(user_id=u_admin.id, role_id=r_admin.id))
    db_session.commit()
    
    # Generate token
    access_token = create_access_token(data={"sub": u_admin.email})
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client
