from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

from routers import course
from routers import room_allocation
from routers import student
from routers import student_course

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

app.include_router(course.router)
app.include_router(room_allocation.router)
app.include_router(student.router)
app.include_router(student_course.router)