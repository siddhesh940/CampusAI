"""
Storage Service

Handles file upload/download operations.
Uses Supabase Storage when configured, falls back to local file storage.
"""

import os
import uuid

import aiofiles
from fastapi import HTTPException, UploadFile, status

from app.config import get_settings

settings = get_settings()

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/jpg",
}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# Local uploads directory (fallback)
LOCAL_UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")


def _supabase_available() -> bool:
    """Check if Supabase credentials are properly configured."""
    return bool(
        settings.SUPABASE_URL
        and settings.SUPABASE_URL.startswith("https://")
        and settings.SUPABASE_SERVICE_ROLE_KEY
    )


def _get_supabase_client():
    """Create a Supabase client with service role key for privileged ops."""
    from supabase import create_client
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


class StorageService:
    """File storage operations (Supabase or local fallback)."""

    @staticmethod
    async def upload_file(
        file: UploadFile, path: str, bucket: str | None = None
    ) -> tuple[str, int]:
        """
        Upload a file. Returns (public_url, file_size).
        Tries Supabase first; falls back to local storage on failure.
        """
        bucket = bucket or settings.SUPABASE_STORAGE_BUCKET

        # Validate file type
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type '{file.content_type}' not allowed. Accepted: PDF, JPG, PNG.",
            )

        # Read and validate size
        contents = await file.read()
        file_size = len(contents)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum of {MAX_FILE_SIZE // (1024 * 1024)}MB.",
            )

        # Generate unique filename
        ext = file.filename.rsplit(".", 1)[-1] if file.filename and "." in file.filename else "bin"
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        unique_path = f"{path}/{unique_name}"

        # Try Supabase first
        if _supabase_available():
            try:
                client = _get_supabase_client()
                client.storage.from_(bucket).upload(
                    path=unique_path,
                    file=contents,
                    file_options={"content-type": file.content_type},
                )
                public_url = client.storage.from_(bucket).get_public_url(unique_path)
                return public_url, file_size
            except Exception:
                pass  # Fall through to local storage

        # Local file storage fallback
        try:
            local_dir = os.path.join(LOCAL_UPLOAD_DIR, path.replace("/", os.sep))
            os.makedirs(local_dir, exist_ok=True)
            local_path = os.path.join(local_dir, unique_name)

            async with aiofiles.open(local_path, "wb") as f:
                await f.write(contents)

            # Return a URL that the backend can serve
            public_url = f"/uploads/{unique_path}"
            return public_url, file_size
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload file: {str(e)}",
            )

    @staticmethod
    async def delete_file(path: str, bucket: str | None = None) -> bool:
        """Delete a file from storage."""
        bucket = bucket or settings.SUPABASE_STORAGE_BUCKET

        # Try Supabase
        if _supabase_available():
            try:
                client = _get_supabase_client()
                client.storage.from_(bucket).remove([path])
                return True
            except Exception:
                pass

        # Try local
        local_path = os.path.join(LOCAL_UPLOAD_DIR, path.replace("/", os.sep))
        if os.path.exists(local_path):
            os.remove(local_path)
            return True
        return False

    @staticmethod
    async def get_signed_url(path: str, expires_in: int = 3600) -> str:
        """Get a time-limited signed URL for a private file."""
        if _supabase_available():
            client = _get_supabase_client()
            result = client.storage.from_(
                settings.SUPABASE_STORAGE_BUCKET
            ).create_signed_url(path, expires_in)
            return result.get("signedURL", "")
        # For local files, just return the path
        return f"/uploads/{path}"
