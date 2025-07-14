import os
import re
import base64
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, storage, db

from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
    })


def upload_picture_to_firebase(uploader_id: str, uploader_name: str, event_id: str, data_url: str):
    pictures_ref = db.reference(f"pictures/{event_id}")
    new_picture_ref = pictures_ref.push()
    picture_id = new_picture_ref.key

    match = re.match(r"data:image/(.*?);base64,(.*)", data_url)
    if not match:
        raise ValueError("Invalid data_url format")

    file_ext, encoded = match.groups()
    image_data = base64.b64decode(encoded)

    storage_path = f"pictures/{event_id}/{picture_id}.jpg"
    bucket = storage.bucket()
    blob = bucket.blob(storage_path)
    blob.upload_from_string(image_data, content_type=f"image/{file_ext}")

    blob.make_public()
    download_url = blob.public_url

    created_at = datetime.utcnow().isoformat()
    meta = {
        "id": picture_id,
        "url": download_url,
        "uploaderId": uploader_id,
        "uploaderName": uploader_name,
        "eventId": event_id,
        "createdAt": created_at
    }

    new_picture_ref.set(meta)

    return meta
