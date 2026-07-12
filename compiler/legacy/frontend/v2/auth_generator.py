"""
Aayu Auth Generator (Sprint 33)

Generates Identity & Access Management files:
- auth.py (JWT encoding/decoding, password hashing)
- routers/auth.py (Login, Register endpoints)
"""
from typing import Dict
from .schema_nodes import SchemaModel

class AuthGenerator:
    def generate(self, schema: SchemaModel) -> Dict[str, str]:
        files = {}
        files["auth.py"] = self._gen_auth_utils(schema)
        files["routers/auth.py"] = self._gen_auth_router(schema)
        return files

    def _gen_auth_utils(self, schema: SchemaModel) -> str:
        lines = [
            "from datetime import datetime, timedelta",
            "from typing import Optional",
            "from jose import JWTError, jwt",
            "from passlib.context import CryptContext",
            "from fastapi import Depends, HTTPException, status",
            "from sqlalchemy.orm import Session",
            "from database import get_db",
            "from models import User",
            "",
            "# Secret keys and algorithms should be in .env, hardcoded here for V1",
            "SECRET_KEY = \"aayu_super_secret_key\"",
            "ALGORITHM = \"HS256\"",
            "ACCESS_TOKEN_EXPIRE_MINUTES = 30",
            "",
            "pwd_context = CryptContext(schemes=[\"bcrypt\"], deprecated=\"auto\")",
            "",
            "def verify_password(plain_password, hashed_password):",
            "    return pwd_context.verify(plain_password, hashed_password)",
            "",
            "def get_password_hash(password):",
            "    return pwd_context.hash(password)",
            "",
            "def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):",
            "    to_encode = data.copy()",
            "    if expires_delta:",
            "        expire = datetime.utcnow() + expires_delta",
            "    else:",
            "        expire = datetime.utcnow() + timedelta(minutes=15)",
            "    to_encode.update({\"exp\": expire})",
            "    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)",
            "    return encoded_jwt",
            ""
        ]
        
        if schema.has_rbac:
            rbac_lines = [
                "from fastapi.security import OAuth2PasswordBearer",
                "oauth2_scheme = OAuth2PasswordBearer(tokenUrl=\"auth/login\")",
                "",
                "def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):",
                "    credentials_exception = HTTPException(",
                "        status_code=status.HTTP_401_UNAUTHORIZED,",
                "        detail=\"Could not validate credentials\",",
                "        headers={\"WWW-Authenticate\": \"Bearer\"},",
                "    )",
                "    try:",
                "        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])",
                "        email: str = payload.get(\"sub\")",
                "        if email is None:",
                "            raise credentials_exception",
                "    except JWTError:",
                "        raise credentials_exception",
                "    user = db.query(User).filter(User.email == email).first()",
                "    if user is None:",
                "        raise credentials_exception",
                "    return user",
                "",
                "def require_permission(required_permission: str):",
                "    def permission_checker(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):",
                "        from models import Role, Permission, UserRole, RolePermission",
                "        # Fetch all permissions for the user's roles",
                "        user_roles = db.query(Role).join(UserRole, UserRole.role_id == Role.id).filter(UserRole.user_id == current_user.id).all()",
                "        for r in user_roles:",
                "            perms = db.query(Permission).join(RolePermission, RolePermission.permission_id == Permission.id).filter(RolePermission.role_id == r.id).all()",
                "            if any(p.name == required_permission for p in perms):",
                "                return current_user",
                "        raise HTTPException(status_code=403, detail=\"Operation not permitted\")",
                "    return permission_checker",
                ""
            ]
            lines.extend(rbac_lines)
            
        return "\n".join(lines)

    def _gen_auth_router(self, schema: SchemaModel) -> str:
        lines = [
            "from fastapi import APIRouter, Depends, HTTPException, status",
            "from sqlalchemy.orm import Session",
            "from pydantic import BaseModel",
            "import uuid",
            "from typing import List, Optional",
            "",
            "from database import get_db",
            "from models import User",
            "from auth import verify_password, get_password_hash, create_access_token",
            "",
            "router = APIRouter(prefix=\"/auth\", tags=[\"auth\"])",
            "",
            "class AuthRequest(BaseModel):",
            "    email: str",
            "    password: str",
            "",
            "class TokenResponse(BaseModel):",
            "    access_token: str",
            "    token_type: str"
        ]
        
        if schema.has_rbac:
            lines.append("    roles: List[str] = []")
            lines.append("    permissions: List[str] = []")
            
        lines.extend([
            "",
            "@router.post(\"/register\", response_model=TokenResponse)",
            "def register(request: AuthRequest, db: Session = Depends(get_db)):",
            "    db_user = db.query(User).filter(User.email == request.email).first()",
            "    if db_user:",
            "        raise HTTPException(status_code=400, detail=\"Email already registered\")",
            "        ",
            "    hashed_password = get_password_hash(request.password)",
            "    new_user = User(id=str(uuid.uuid4()), email=request.email, password_hash=hashed_password)",
            "    db.add(new_user)",
            "    db.commit()",
            "    db.refresh(new_user)",
            "    ",
            "    access_token = create_access_token(data={\"sub\": new_user.email})",
        ])
        
        if schema.has_rbac:
            lines.extend([
                "    return {\"access_token\": access_token, \"token_type\": \"bearer\", \"roles\": [], \"permissions\": []}"
            ])
        else:
            lines.extend([
                "    return {\"access_token\": access_token, \"token_type\": \"bearer\"}"
            ])
            
        lines.extend([
            "",
            "@router.post(\"/login\", response_model=TokenResponse)",
            "def login(request: AuthRequest, db: Session = Depends(get_db)):",
            "    user = db.query(User).filter(User.email == request.email).first()",
            "    if not user or not verify_password(request.password, user.password_hash):",
            "        raise HTTPException(",
            "            status_code=status.HTTP_401_UNAUTHORIZED,",
            "            detail=\"Incorrect email or password\",",
            "            headers={\"WWW-Authenticate\": \"Bearer\"},",
            "        )",
            "        ",
            "    access_token = create_access_token(data={\"sub\": user.email})",
        ])
        
        if schema.has_rbac:
            lines.extend([
                "    from models import Role, Permission, UserRole, RolePermission",
                "    user_roles = db.query(Role).join(UserRole, UserRole.role_id == Role.id).filter(UserRole.user_id == user.id).all()",
                "    roles = [r.name for r in user_roles]",
                "    permissions = []",
                "    for r in user_roles:",
                "        perms = db.query(Permission).join(RolePermission, RolePermission.permission_id == Permission.id).filter(RolePermission.role_id == r.id).all()",
                "        permissions.extend([p.name for p in perms])",
                "    return {\"access_token\": access_token, \"token_type\": \"bearer\", \"roles\": roles, \"permissions\": list(set(permissions))}"
            ])
        else:
            lines.extend([
                "    return {\"access_token\": access_token, \"token_type\": \"bearer\"}"
            ])
            
        return "\n".join(lines)
