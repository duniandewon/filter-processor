import base64
from PIL import Image
import io

from fastapi import HTTPException
from firebase_admin import db


def validate_data_url_image(data_url: str):
    """
    Validate that a data_url is a valid image.
    Returns decoded binary image data if valid.
    Raises HTTPException if invalid.
    """

    if not data_url.startswith("data:image/"):
        raise HTTPException(
            status_code=400,
            detail="Not a valid image data URL."
        )

    try:
        _, encoded = data_url.split(",", 1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid data URL format.")

    try:
        decoded = base64.b64decode(encoded)
    except base64.binascii.Error:
        raise HTTPException(status_code=400, detail="Invalid base64 encoding.")

    try:
        image = Image.open(io.BytesIO(decoded))
        image.verify()
    except Exception:
        raise HTTPException(
            status_code=400, detail="Invalid or corrupted image file.")


def verify_participant(event_id: str, uploader_id: str):
    """
    Checks if the given uploader_id is in the participants list for the event.
    Raises HTTPException if not.
    """
    ref = db.reference(f"events/{event_id}/participants")
    participants = ref.get() or []

    if uploader_id not in participants:
        raise HTTPException(
            status_code=403, detail="Uploader is not a participant.")

    return True
