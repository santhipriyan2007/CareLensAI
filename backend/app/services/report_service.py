from uuid import UUID

from fastapi import HTTPException, UploadFile, status

from app.database.supabase import supabase
from app.schemas.report import ReportListResponse, ReportResponse
from app.schemas.user import UserResponse
from app.storage.storage_service import StorageService


class ReportService:

    @staticmethod
    async def create_report(
        file: UploadFile,
        patient_user_id: UUID,
        uploaded_by_user_id: UUID,
    ) -> ReportResponse:
        """
        Upload a medical report for a patient.
        """

        patient = (
            supabase.table("users")
            .select("*")
            .eq("id", str(patient_user_id))
            .execute()
        )

        if not patient.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found.",
            )

        if patient.data[0]["role"] != "patient":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selected user is not a patient.",
            )

        upload_data = await StorageService.upload_file(file)

        response = (
            supabase.table("reports")
            .insert(
                {
                    "patient_user_id": str(patient_user_id),
                    "uploaded_by_user_id": str(uploaded_by_user_id),
                    "original_file_name": upload_data["original_file_name"],
                    "stored_file_name": upload_data["stored_file_name"],
                    "file_type": upload_data["file_type"],
                    "file_size": upload_data["file_size"],
                    "storage_path": upload_data["storage_path"],
                }
            )
            .execute()
        )

        report = response.data[0]

        return ReportResponse(
            id=report["id"],
            patient_user_id=report["patient_user_id"],
            uploaded_by_user_id=report["uploaded_by_user_id"],
            original_file_name=report["original_file_name"],
            file_type=report["file_type"],
            file_size=report["file_size"],
            uploaded_at=report["uploaded_at"],
            download_url=None,
        )

    @staticmethod
    async def get_reports(
        current_user: UserResponse,
    ) -> ReportListResponse:

        query = (
            supabase.table("reports")
            .select("*")
            .order("uploaded_at", desc=True)
        )

        if current_user.role == "patient":
            query = query.eq(
                "patient_user_id",
                str(current_user.id),
            )

        response = query.execute()

        reports = [
            ReportResponse(
                id=report["id"],
                patient_user_id=report["patient_user_id"],
                uploaded_by_user_id=report["uploaded_by_user_id"],
                original_file_name=report["original_file_name"],
                file_type=report["file_type"],
                file_size=report["file_size"],
                uploaded_at=report["uploaded_at"],
                download_url=None,
            )
            for report in response.data
        ]

        return ReportListResponse(
            total=len(reports),
            reports=reports,
        )

    @staticmethod
    def _get_authorized_report(
        report_id: UUID,
        current_user: UserResponse,
    ) -> dict:
        """
        Retrieve a report and verify that the current user
        is authorized to access it.
        """

        response = (
            supabase.table("reports")
            .select("*")
            .eq("id", str(report_id))
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found.",
            )

        report = response.data[0]

        if (
            current_user.role == "patient"
            and report["patient_user_id"] != str(current_user.id)
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this report.",
            )

        return report

    @staticmethod
    async def get_report_by_id(
        report_id: UUID,
        current_user: UserResponse,
    ) -> ReportResponse:

        report = ReportService._get_authorized_report(
            report_id,
            current_user,
        )

        return ReportResponse(
            id=report["id"],
            patient_user_id=report["patient_user_id"],
            uploaded_by_user_id=report["uploaded_by_user_id"],
            original_file_name=report["original_file_name"],
            file_type=report["file_type"],
            file_size=report["file_size"],
            uploaded_at=report["uploaded_at"],
            download_url=None,
        )

    @staticmethod
    async def get_signed_url(
        report_id: UUID,
        current_user: UserResponse,
    ) -> dict:
        """
        Generate a signed URL after authorization.
        """

        report = ReportService._get_authorized_report(
            report_id,
            current_user,
        )

        signed_url = StorageService.generate_signed_url(
            report["storage_path"]
        )

        return {
            "download_url": signed_url
        }