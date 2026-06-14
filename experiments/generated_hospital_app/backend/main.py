from fastapi import FastAPI
from .database import engine
from . import models

from .routers import patient
from .routers import doctor

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Aayu Generated Application')

@app.get('/')
def health_check():
    return {'status': 'ok'}

app.include_router(patient.router)
app.include_router(doctor.router)