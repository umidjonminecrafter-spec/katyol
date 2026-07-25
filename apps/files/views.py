import os
import uuid
from datetime import datetime
from fastapi import Depends, UploadFile, File, HTTPException, status
from core.config import settings
from core.dependencies import get_current_user
from apps.accounts.models import User

async def upload_file_view(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fayl formati qo'llab-quvvatlanmaydi. Ruxsat etilgan: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fayl hajmi {settings.MAX_FILE_SIZE_MB}MB dan oshmasligi kerak"
        )

    now = datetime.now()
    year_str = now.strftime("%Y")
    month_str = now.strftime("%m")

    upload_path = os.path.join(settings.UPLOAD_DIR, year_str, month_str)
    os.makedirs(upload_path, exist_ok=True)

    unique_filename = f"{uuid.uuid4()}{ext}"
    full_filepath = os.path.join(upload_path, unique_filename)

    with open(full_filepath, "wb") as f:
        f.write(content)

    url_path = f"/uploads/{year_str}/{month_str}/{unique_filename}"

    return {
        "success": True,
        "data": {
            "filename": file.filename,
            "url": url_path,
            "size_bytes": len(content),
            "mime_type": file.content_type
        }
    }
