from fastapi import APIRouter
from typing import List
from app.models import ${model_imports}

router = APIRouter()

${routers_content}
