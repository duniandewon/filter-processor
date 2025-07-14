from fastapi import APIRouter
from app.api.v1 import pictures

router = APIRouter(prefix="/api/v1")

router.include_router(
    pictures.router,
    prefix="/pictures",
    tags=["event pictures"]
)
