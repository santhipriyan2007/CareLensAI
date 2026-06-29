from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Clinical Decision Support & Medical Report Analysis Platform",
)

app.include_router(api_router)