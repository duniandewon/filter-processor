from fastapi import APIRouter, HTTPException
from app.models.picture import UploadPictureRequest
from app.services.firebase_service import upload_picture_to_firebase

router = APIRouter()

@router.post("/")
async def upload_picture(payload: UploadPictureRequest):
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