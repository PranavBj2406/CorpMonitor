from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging
from app.core.config import settings
from app.api.routes import router
setup_logging()
app = FastAPI(
    title=settings.API_TITLE,
    description="Extract director appointment and resignation information from ZIP archives containing PDFs.",
    version=settings.API_VERSION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router, prefix="/api", tags=["Extraction"])


@app.get("/")
async def root():
    return {
        "message": "Director Change Extraction API",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }