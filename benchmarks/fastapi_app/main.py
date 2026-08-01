from fastapi import FastAPI, Depends, HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import jwt
import time
import uuid

# Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./benchmark_fastapi.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBProduct(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer)

class DBOrder(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    quantity = Column(Integer)
    total = Column(Float)

Base.metadata.create_all(bind=engine)

# App
app = FastAPI(title="FastAPI Benchmark")

# Auth
security = HTTPBearer()
JWT_SECRET = "fastapi_super_secret_v1"

def mint_jwt(payload: dict) -> str:
    if "exp" not in payload:
        payload["exp"] = int(time.time()) + 86400
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# Models
class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class OrderCreate(BaseModel):
    product_id: int
    quantity: int
    total: float

class LoginCreate(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/health")
def health():
    return {"success": True, "data": {"status": "ok"}}

@app.post("/api/login")
def login(payload: LoginCreate):
    # Mock authentication match
    token = mint_jwt({"email": payload.email, "id": 1, "roles": [], "permissions": []})
    return {"success": True, "data": token}

@app.get("/api/products")
def list_products(db: Session = Depends(get_db), payload: dict = Depends(verify_jwt)):
    products = db.query(DBProduct).limit(20).all()
    # Formatting to exactly match AAYU structure
    data = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]
    return {"success": True, "data": data, "meta": {"total": len(products), "page": 1, "limit": 20}}

@app.post("/api/products", status_code=201)
def create_product(prod: ProductCreate, db: Session = Depends(get_db), payload: dict = Depends(verify_jwt)):
    db_prod = DBProduct(**prod.model_dump())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return {"success": True, "data": {"id": db_prod.id, "name": db_prod.name, "price": db_prod.price, "stock": db_prod.stock}}

@app.get("/api/orders")
def list_orders(db: Session = Depends(get_db), payload: dict = Depends(verify_jwt)):
    orders = db.query(DBOrder).limit(20).all()
    data = [{"id": o.id, "product_id": o.product_id, "quantity": o.quantity, "total": o.total} for o in orders]
    return {"success": True, "data": data, "meta": {"total": len(orders), "page": 1, "limit": 20}}

@app.post("/api/orders", status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db), payload: dict = Depends(verify_jwt)):
    db_order = DBOrder(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return {"success": True, "data": {"id": db_order.id, "product_id": db_order.product_id, "quantity": db_order.quantity, "total": db_order.total}}
