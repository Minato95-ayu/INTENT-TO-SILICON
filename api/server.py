from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from v1.compile import router as compile_router
from v1.brainos import router as brainos_router
from v1.health import router as health_router

app = FastAPI(title="AAYU API", version="1.0.0-rc1")

# Configure CORS for Playground
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to aayu.dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register v1 routes
app.include_router(health_router, prefix="/api/v1")
app.include_router(compile_router, prefix="/api/v1")
app.include_router(brainos_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    # Run the API on port 8000
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
