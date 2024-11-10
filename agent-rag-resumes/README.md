# Resume RAG Agent

This is an implementation of a Resume Analysis agent using FastAPI and RAG (Retrieval Augmented Generation). The agent provides a standardized interface for processing resume-related queries and work requests.

## Features

- Resume analysis and parsing
- Question answering about resumes
- Resume comparison and matching
- Skills extraction and analysis

## API Endpoints

- `POST /agent/restart` - Starts/restarts the agent
- `POST /agent/message` - Sends a message to the agent
- `GET /agent/status` - Gets the agent status
- `POST /agent/work-request` - Sends a work request to the agent

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Running with Docker

1. Build the Docker image:
```bash
docker build -t resume-rag-agent .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 resume-rag-agent
```

## Environment Variables

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `RESUME_INDEX_PATH`: Path to store resume index (default: data/resume_index)

## API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 