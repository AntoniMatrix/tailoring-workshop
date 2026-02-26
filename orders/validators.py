"""
Validation helpers for security and data quality.
"""

from django.core.exceptions import ValidationError

ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".zip"}
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10MB


def validate_upload(file_obj) -> None:
    """
    Validate uploaded file:
    - size limit
    - allowed extension
    """
    name = (file_obj.name or "").lower()
    size = getattr(file_obj, "size", 0)

    if size and size > MAX_UPLOAD_SIZE_BYTES:
        raise ValidationError("File too large (max 10MB).")

    dot = name.rfind(".")
    ext = name[dot:] if dot != -1 else ""
    if ext not in ALLOWED_UPLOAD_EXTENSIONS:
        raise ValidationError("Unsupported file type.")