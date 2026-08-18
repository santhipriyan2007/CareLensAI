from fastapi import HTTPException, status

from app.database.supabase import supabase
from app.schemas.user import UserResponse


class PatientService:

    @staticmethod
    async def get_patients() -> list[UserResponse]:
        """
        Retrieve all users with the patient role.
        """

        response = (
            supabase.table("users")
            .select("id, full_name, email, role")
            .eq("role", "patient")
            .order("full_name")
            .execute()
        )

        if not response.data:
            return []

        return [
            UserResponse(**patient)
            for patient in response.data
        ]