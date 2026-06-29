from fastapi import APIRouter

router = APIRouter(
    tags=["Health"]
)


@router.get("/")
def root():
    return {
        "message": "Welcome to CareLens AI API"
    }


@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }