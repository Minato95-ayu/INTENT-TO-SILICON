from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

from routers import product
from routers import order
from routers import product_order

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Aayu Generated Application')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def health_check():
    return {'status': 'ok'}

app.include_router(product.router)
app.include_router(order.router)
app.include_router(product_order.router)