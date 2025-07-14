from pydantic import BaseModel


class UploadPictureRequest(BaseModel):
    uploaderId: str
    uploaderName: str
    eventId: str
    picture: str  # base64 data_url
