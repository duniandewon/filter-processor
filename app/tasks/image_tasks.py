import base64
from typing import Any, Dict

from app.core.celery_app import celery_app
from app.services.ffmpeg_service import apply_lut_with_ffmpeg
from app.services.firebase_service import upload_picture_to_firebase
from celery import current_task


@celery_app.task(bind=True)
def process_and_upload_image(
    self,
    uploader_id: str,
    uploader_name: str,
    event_id: str,
    filter_name: str,
    picture_data: str,
    file_ext: str
) -> Dict[str, Any]:
    try:
        current_task.update_state(
            state='PROCESSING',
            meta={'current': 1, 'total': 3, 'status': 'Decoding image...'}
        )

        original_bytes = base64.b64decode(picture_data)

        current_task.update_state(
            state='PROCESSING',
            meta={'current': 2, 'total': 3, 'status': 'Applying filter...'}
        )

        cube_file_path = f"app/filters/{filter_name}.cube"
        filtered_bytes = apply_lut_with_ffmpeg(
            input_bytes=original_bytes,
            cube_file_path=cube_file_path
        )

        current_task.update_state(
            state='PROCESSING',
            meta={
                'current': 3,
                'total': 3,
                'status': 'Uploading to Firebase...'
            }
        )

        result = upload_picture_to_firebase(
            uploader_id=uploader_id,
            uploader_name=uploader_name,
            event_id=event_id,
            image_bytes=filtered_bytes,
            file_ext=file_ext
        )

        return {
            'status': 'SUCCESS',
            'result': result,
            'message': 'Image processed and uploaded successfully'
        }
    except Exception as e:
        current_task.update_state(
            state='FAILURE',
            meta={'error': str(e), 'message': 'Failed to process image'}
        )
        raise e
