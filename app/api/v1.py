from fastapi import APIRouter, UploadFile, File

router = APIRouter(
    prefix="/api/v1",
    tags=["Image Processing"],
)


@router.post("/process")
async def process_image(
    image: UploadFile = File(...),
    preset: UploadFile = File(...)
):
    image_path = f"storage/uploads/{image.filename}"
    preset_path = f"storage/uploads/{preset.filename}"

    with open(image_path, "wb") as img_file:
        img_file.write(await image.read())

    with open(preset_path, "wb") as preset_file:
        preset_file.write(await preset.read())

    return {
        "message": "Files received and saved successfully!",
        "image_path": image_path,
        "preset_path": preset_path
    }
