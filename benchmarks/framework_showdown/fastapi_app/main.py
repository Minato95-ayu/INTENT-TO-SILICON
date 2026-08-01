from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import sqlite3
import jwt
from typing import List, Optional
import datetime
import os

app = FastAPI(title="Benchmark Shop", version="1.0.0")

SECRET_KEY = "benchmark_secret"

def get_db():
    conn = sqlite3.connect("fastapi.db")
    conn.row_factory = sqlite3.Row
    return conn

# Init DB
conn = get_db()
conn.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, role TEXT)''')
conn.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER)''')
try:
    conn.execute("INSERT INTO users (email, password, role) VALUES ('admin@shop.com', 'secret', 'admin')")
except sqlite3.IntegrityError:
    pass
conn.commit()
conn.close()

# Schemas
class LoginReq(BaseModel):
    email: str
    password: str

class ProductBase(BaseModel):
    name: str
    price: float
    stock: int

class ProductResp(ProductBase):
    id: int

# Auth Dependency
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")

def verify_admin(token: str):
    payload = verify_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return payload

@app.post("/api/login")
def login(req: LoginReq):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email=? AND password=?", (req.email, req.password)).fetchone()
    if user:
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        token = jwt.encode({"sub": user["email"], "role": user["role"], "exp": exp}, SECRET_KEY, algorithm="HS256")
        return {"success": True, "token": token}
    raise HTTPException(status_code=401, detail="Invalid Credentials")

@app.get("/api/products", response_model=List[ProductResp])
def list_products():
    conn = get_db()
    rows = conn.execute("SELECT * FROM products").fetchall()
    return [dict(r) for r in rows]

@app.post("/api/products", response_model=ProductResp)
def create_product(prod: ProductBase, token: str):
    verify_admin(token)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (prod.name, prod.price, prod.stock))
    conn.commit()
    return {**prod.dict(), "id": cursor.lastrowid}

@app.get("/api/products/{pid}", response_model=ProductResp)
def get_product(pid: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Not Found")
    return dict(row)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=False)
