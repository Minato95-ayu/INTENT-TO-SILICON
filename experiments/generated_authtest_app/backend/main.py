from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

from routers import auth
from routers import patient
from routers import appointment
from routers import user
from routers import role

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

app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(appointment.router)
app.include_router(user.router)
app.include_router(role.router)