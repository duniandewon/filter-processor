from pydantic import BaseModel


class UploadPictureRequest(BaseModel):
    uploaderId: str
    uploaderName: str
    eventId: str
    filter_name: str
    picture: str  # base64 data_url

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str