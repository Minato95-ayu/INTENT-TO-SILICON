import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from database import engine
from logger import get_logger
import models

from routers import auth
from routers import patient
from routers import appointment
from routers import user
from routers import role
from routers import permission
from routers import user_role
from routers import role_permission

logger = get_logger('main')

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Aayu Generated Application')

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers['X-Request-ID'] = request_id
        return response

app.add_middleware(RequestIdMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, 'request_id', 'unknown')
    logger.error(f'Unhandled exception: {str(exc)}', exc_info=True, extra={'request_id': request_id})
    return JSONResponse(
        status_code=500,
        content={'error': 'Internal Server Error', 'request_id': request_id}
    )

@app.get('/')
def health_check():
    return {'status': 'ok'}

app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(appointment.router)
app.include_router(user.router)
app.include_router(role.router)
app.include_router(permission.router)
app.include_router(user_role.router)
app.include_router(role_permission.router)