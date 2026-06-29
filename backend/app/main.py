from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
    title="CareLens AI API",
    description="AI-powered Clinical Decision Support & Medical Report Analysis Platform",
    version="1.0.0",
)

app.include_router(api_router)