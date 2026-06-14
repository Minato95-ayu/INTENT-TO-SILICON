from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

from routers import patient
from routers import doctor
from routers import appointment

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

app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointment.router)