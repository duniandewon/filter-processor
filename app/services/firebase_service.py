import os
import json
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, storage, db

from dotenv import load_dotenv

load_dotenv()

firebase_service_account_json_string = os.getenv(
    "FIREBASE_SERVICE_ACCOUNT_KEY_JSON")

if firebase_service_account_json_string:
    try:
        service_account_info = json.loads(firebase_service_account_json_string)
        cred = credentials.Certificate(service_account_info)
    except json.JSONDecodeError:
        print("Error: Could not decode FIREBASE_SERVICE_ACCOUNT_KEY_JSON. Check your .env file format.")
        exit(1)
else:
    print("ERROR: The 'FIREBASE_SERVICE_ACCOUNT_KEY_JSON' environment variable is not set.")
    print("Please ensure you have set this environment variable in your .env file (for local development) ")
    print("or in your deployment environment (e.g., Railway variables) with the content of your service account key.")
    exit(1)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
    })


def upload_picture_to_firebase(
    uploader_id: str,
    uploader_name: str,
    event_id: str,
    image_bytes: bytes,
    file_ext: str = "jpg"
):
    pictures_ref = db.reference(f"pictures/{event_id}")
    new_picture_ref = pictures_ref.push()
    picture_id = new_picture_ref.key

    storage_path = f"pictures/{event_id}/{picture_id}.jpg"

    bucket = storage.bucket()
    blob = bucket.blob(storage_path)
    blob.upload_from_string(image_bytes, content_type=f"image/{file_ext}")

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
