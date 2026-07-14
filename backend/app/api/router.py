from fastapi import APIRouter

from app.api.routes.analysis import router as analysis_router
from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.history import router as history_router
from app.api.routes.ocr import router as ocr_router
from app.api.routes.report import router as report_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(report_router)
api_router.include_router(ocr_router)
api_router.include_router(analysis_router)
api_router.include_router(history_router)