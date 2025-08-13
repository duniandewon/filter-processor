import re

from app.core.celery_app import celery_app
from app.models.picture import TaskResponse, UploadPictureRequest
from app.tasks.image_tasks import process_and_upload_image
from app.utils.validators import validate_data_url_image, verify_participant
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/")
async def upload_picture(payload: UploadPictureRequest):
    verify_participant(payload.eventId, payload.uploaderId)

    validate_data_url_image(payload.picture)

    match = re.match(r"data:image/(.*?);base64,(.*)", payload.picture)
    if not match:
        raise ValueError("Invalid data_url format")

    file_ext, encoded = match.groups()

    if not re.compile(r"^[a-zA-Z0-9_]+$").match(payload.filter_name):
        raise HTTPException(
            status_code=400,
            detail="Invalid filter name. Only letters, numbers, and underscores allowed."
        )

    task = process_and_upload_image.delay(
        uploader_id=payload.uploaderId,
        uploader_name=payload.uploaderName,
        event_id=payload.eventId,
        filter_name=payload.filter_name,
        picture_data=encoded,
        file_ext=file_ext
    )

    return TaskResponse(
        task_id=task.id,
        status="PENDING",
        message="Image processing started"
    )
