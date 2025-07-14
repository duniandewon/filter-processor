from fastapi import APIRouter, HTTPException
from app.models.picture import UploadPictureRequest
from app.services.firebase_service import upload_picture_to_firebase

from app.utils.validators import validate_data_url_image, verify_participant

router = APIRouter()


@router.post("/")
async def upload_picture(payload: UploadPictureRequest):
    verify_participant(payload.eventId, payload.uploaderId)

    validate_data_url_image(payload.picture)

    try:
        result = upload_picture_to_firebase(
            uploader_id=payload.uploaderId,
            uploader_name=payload.uploaderName,
            event_id=payload.eventId,
            data_url=payload.picture
        )
        return result

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
