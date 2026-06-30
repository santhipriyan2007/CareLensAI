from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user
from app.schemas.token import TokenResponse
from app.schemas.user import (
    LoginRequest,
    RegisterRequest,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user: RegisterRequest):
    """
    Register a new user.
    """
    try:
        return AuthService.register_user(user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(user: LoginRequest):
    """
    Authenticate a user.
    """
    try:
        return AuthService.login_user(user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user=Depends(get_current_user),
):
    """
    Get the currently authenticated user.
    """
    return UserResponse(**current_user)


from app.core.dependencies import (
    get_current_user,
    require_role,
)


@router.get("/admin")
def admin_dashboard(
    current_user=Depends(
        require_role("admin")
    ),
):
    return {
        "message": "Welcome Admin!",
        "user": UserResponse(**current_user),
    }


@router.get("/doctor")
def doctor_dashboard(
    current_user=Depends(
        require_role("doctor")
    ),
):
    return {
        "message": "Welcome Doctor!",
        "user": UserResponse(**current_user),
    }


@router.get("/patient")
def patient_dashboard(
    current_user=Depends(
        require_role("patient")
    ),
):
    return {
        "message": "Welcome Patient!",
        "user": UserResponse(**current_user),
    }