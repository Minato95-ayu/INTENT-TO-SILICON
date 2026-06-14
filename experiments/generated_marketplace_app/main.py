from fastapi import FastAPI
from .database import engine
from . import models

from .routers import product
from .routers import order
from .routers import product_order

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Aayu Generated Application')

@app.get('/')
def health_check():
    return {'status': 'ok'}

app.include_router(product.router)
app.include_router(order.router)
app.include_router(product_order.router)