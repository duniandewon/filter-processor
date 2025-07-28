import base64
import re

from fastapi import APIRouter, HTTPException

from app.models.picture import UploadPictureRequest

from app.services.firebase_service import upload_picture_to_firebase
from app.services.ffmpeg_service import apply_lut_with_ffmpeg

from app.utils.validators import validate_data_url_image, verify_participant

router = APIRouter()


@router.post("/")
async def upload_picture(payload: UploadPictureRequest):
    verify_participant(payload.eventId, payload.uploaderId)

    validate_data_url_image(payload.picture)

    match = re.match(r"data:image/(.*?);base64,(.*)", payload.picture)
    if not match:
        raise ValueError("Invalid data_url format")

    file_ext, encoded = match.groups()
    original_bytes = base64.b64decode(encoded)

    if not re.compile(r"^[a-zA-Z0-9_]+$").match(payload.filter_name):
        raise HTTPException(
            status_code=400,
            detail="Invalid filter name. Only letters, numbers, and underscores allowed."
        )

    cube_file_path = f"app/filters/{payload.filter_name}.cube"

    try:
        filtered_bytes = apply_lut_with_ffmpeg(
            input_bytes=original_bytes,
            cube_file_path=cube_file_path
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to apply filter: {e}")

    result = upload_picture_to_firebase(
        uploader_id=payload.uploaderId,
        uploader_name=payload.uploaderName,
        event_id=payload.eventId,
        image_bytes=filtered_bytes,
        file_ext=file_ext
    )

    return result
