# Evo Concierge Agent

This is an implementation of an Evo system agent using FastAPI. The agent provides a standardized interface for processing messages and work requests.

## API Endpoints

- `POST /agent/restart` - Starts/restarts the agent
- `POST /agent/message` - Sends a message to the agent
- `GET /agent/status` - Gets the agent status
- `POST /agent/work-request` - Sends a work request to the agent

## Running Locally (Without Docker)

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
docker build -t evo-concierge .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 evo-concierge
```

## API Documentation

Once the server is running, you can access the interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Usage Examples

### Restart Agent
```bash
curl -X POST http://localhost:8000/agent/restart
```

### Send Message
```bash
curl -X POST http://localhost:8000/agent/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello agent",
    "role": "user",
    "context": {},
    "history": []
  }'
```

### Get Status
```bash
curl http://localhost:8000/agent/status
```

### Send Work Request
```bash
curl -X POST http://localhost:8000/agent/work-request \
  -H "Content-Type: application/json" \
  -d '{
    "task": "analyze data",
    "context": {},
    "history": []
  }'
```

## Response Format

All API responses follow this general structure:
```json
{
  "status": "completed",
  "result": "Operation result message",
  "error": null
}
```

## Environment Variables

The following environment variables can be configured:

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

You can set these by creating a `.env` file in the root directory.