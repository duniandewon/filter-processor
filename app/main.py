from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add production domain later, e.g.:
    # "https://my-shared-album-app.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
