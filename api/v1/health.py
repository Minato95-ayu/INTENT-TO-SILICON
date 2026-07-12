from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "compiler": "ready",
        "brainos": "ready",
        "intent_engine": "ready",
        "version": "1.0.0-rc1"
    }
