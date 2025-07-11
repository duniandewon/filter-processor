from fastapi import FastAPI
from app.api import v1

app = FastAPI(
    title="Image Processor API",
    version="1.0.0",
)

app.include_router(v1.router)