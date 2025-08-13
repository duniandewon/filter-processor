# Image Filter Processing API

A FastAPI application with Celery background task processing for applying LUT filters to images and uploading them to Firebase.

## Features

- **RESTful API** for image upload and processing
- **Background task processing** with Celery and Redis
- **LUT filter application** using FFmpeg
- **Firebase integration** for image storage
- **Real-time monitoring** with Flower
- **Dockerized deployment** ready for Railway

## Architecture

```md
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ FastAPI App │───▶│ Redis Broker │───▶│ Celery Workers │
│ (HTTP API) │ │ (Message │ │ (Background │
│ │ │ Queue) │ │ Tasks) │
└─────────────────┘ └─────────────────┘ └─────────────────┘
│ │ │
│ │ ▼
│ │ ┌─────────────────┐
│ │ │ Firebase Storage│
│ │ │ (Image Upload) │
▼ ▼ └─────────────────┘
┌─────────────────┐ ┌─────────────────┐
│ Flower │ │ Task Results │
│ (Monitoring) │ │ (Redis DB) │
└─────────────────┘ └─────────────────┘
```

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Celery** - Distributed task queue
- **Redis** - Message broker and result backend
- **FFmpeg** - Image/video processing
- **Firebase** - Cloud storage and database
- **Docker** - Containerization

## Project Structure

```md
xmp-processor/
├── app/
│ ├── api/
│ │ └── v1/
│ │ └── pictures/
│ ├── core/
│ │ ├── config.py # Application settings
│ │ └── celery_app.py # Celery configuration
│ ├── filters/ # .cube LUT files
│ ├── models/ # Pydantic models
│ ├── services/
│ │ ├── ffmpeg_service.py # Image processing
│ │ └── firebase_service.py # Firebase integration
│ ├── tasks/
│ │ └── image_tasks.py # Celery tasks
│ └── utils/ # Utility functions
├── docker-compose.yml # Multi-service setup
├── Dockerfile # Container definition
├── requirements.txt # Python dependencies
└── README.md
```

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- Firebase project with service account key
- Redis server (or use Docker)

## Quick Start

### 1. Clone the Repository

```Bash
git clone https://github.com/duinandeown/xmp-processor.git

cd xmp-processor
```

### 2. Environment Configuration

Create a `.env` file in the root directory

```Bash
REDIS_URL=REDIS_URL
REDIS_PASSWORD=your_password

FIREBASE_STORAGE_BUCKET=FIREBASE_STORAGE_BUCKET
FIREBASE_DATABASE_URL=FIREBASE_DATABASE_URL
FIREBASE_SERVICE_ACCOUNT_KEY_JSON=

ACKEND_CORS_ORIGINS=json-string
```

### 3. Run with Docker Compose

```Bash
# you may need to use `sudo`

docker compose up
# or
docker-compose up
```

### 4. Access the Application

- **API Documentation**: http://localhost:8000/docs
- **Flower Monitor**: http://localhost:5555
- **API Endpoint**: http://localhost:8000/api/v1/upload

## API Usage

### Upload and Process Image

`POST api/v1/pictures/`

```json
{
  "uploaderId": "user123",
  "uploaderName": "John Doe",
  "eventId": "event456",
  "filter_name": "vintage_filter",
  "picture": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

**Response:**

```json
{
  "task_id": "abc123-def456-789",
  "status": "PENDING",
  "message": "Image processing started"
}
```

## Development

### Local Development Setup

Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start Redis (if not using Docker)

```bash
redis-server
```

Start Celery worker

```bash
celery -A app.core.celery_app worker --loglevel=info
```

Start FastAPI server

```bash
uvicorn app.main:app --reload --port 8000
```

## Adding New LUT Filters

1. Add `.cube` files to the `app/filters/` directory
2. Use the filename (without extension) as the `filter_name` in API requests

## Contact

Feel free to connect with me!

Email: duniandewon@gmail.com

GitHub: [https://github.com/duniandewon](https://github.com/duniandewon)

LinkedIn: [https://linkedin.com/in/duniandewon](https://linkedin.com/in/duniandewon)
