from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.database.supabase import supabase


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 CareLens AI Backend Starting...")

    try:
        supabase.table("users").select("*").limit(1).execute()
        print("✅ Connected to Supabase")
    except Exception as e:
        print(f"❌ Supabase Connection Failed: {e}")

    yield

    print("🛑 CareLens AI Backend Shutting Down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Clinical Decision Support & Medical Report Analysis Platform",
    lifespan=lifespan,
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://care-lens-ai.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API ROUTER
# ============================================================

app.include_router(api_router)