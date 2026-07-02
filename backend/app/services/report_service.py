from fastapi import UploadFile

from app.database.supabase import supabase
from app.storage.storage_service import StorageService


class ReportService:

    @staticmethod
    async def create_report(
        file: UploadFile,
        user_id: str,
    ):

        upload_data = await StorageService.upload_file(file)

        response = (
            supabase.table("reports")
            .insert(
                {
                    "user_id": str(user_id),
                    "original_file_name": upload_data["original_file_name"],
                    "stored_file_name": upload_data["stored_file_name"],
                    "file_type": upload_data["file_type"],
                    "file_size": upload_data["file_size"],
                    "storage_path": upload_data["storage_path"],
                }
            )
            .execute()
        )

        return response.data[0]