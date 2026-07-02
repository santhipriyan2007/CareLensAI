from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.database.supabase import supabase


class StorageService:
    BUCKET_NAME = "medical-reports"

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
    }

    MAX_FILE_SIZE = 10 * 1024 * 1024

    @classmethod
    def validate_file_type(cls, file: UploadFile):
        extension = Path(file.filename).suffix.lower()

        if extension not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type."
            )

    @classmethod
    async def validate_file_size(cls, file: UploadFile):
        content = await file.read()

        if len(content) > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File exceeds maximum size of 10 MB."
            )

        await file.seek(0)

    @classmethod
    def generate_filename(cls, file: UploadFile):
        extension = Path(file.filename).suffix.lower()
        return f"{uuid4()}{extension}"

    @classmethod
    async def upload_file(cls, file: UploadFile):

        cls.validate_file_type(file)
        await cls.validate_file_size(file)

        filename = cls.generate_filename(file)

        storage_path = f"reports/{filename}"

        file_bytes = await file.read()

        try:

            supabase.storage.from_(cls.BUCKET_NAME).upload(
                path=storage_path,
                file=file_bytes,
                file_options={
                    "content-type": file.content_type,
                    "upsert": "false",
                },
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Storage upload failed: {str(e)}"
            )

        await file.seek(0)

        return {
            "original_file_name": file.filename,
            "stored_file_name": filename,
            "storage_path": storage_path,
            "file_type": file.content_type,
            "file_size": len(file_bytes),
        }