from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.database.supabase import supabase
from app.schemas.token import TokenResponse
from app.schemas.user import (
    LoginRequest,
    RegisterRequest,
    UserResponse,
)


class AuthService:
    @staticmethod
    def register_user(user: RegisterRequest) -> UserResponse:
        existing_user = (
            supabase.table("users")
            .select("*")
            .eq("email", user.email)
            .execute()
        )

        if existing_user.data:
            raise ValueError("Email is already registered.")

        password_hash = hash_password(user.password)

        result = (
            supabase.table("users")
            .insert(
                {
                    "full_name": user.full_name,
                    "email": user.email,
                    "password_hash": password_hash,
                    "role": user.role,
                }
            )
            .execute()
        )

        created_user = result.data[0]

        return UserResponse(**created_user)

    @staticmethod
    def login_user(user: LoginRequest) -> TokenResponse:
        result = (
            supabase.table("users")
            .select("*")
            .eq("email", user.email)
            .execute()
        )

        if not result.data:
            raise ValueError("Invalid email or password.")

        db_user = result.data[0]

        if not verify_password(
            user.password,
            db_user["password_hash"],
        ):
            raise ValueError("Invalid email or password.")

        user_response = UserResponse(**db_user)

        access_token = create_access_token(
            {
                "sub": str(user_response.id),
                "email": user_response.email,
                "role": user_response.role,
            }
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response,
        )