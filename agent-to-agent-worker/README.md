# Agent-to-Agent Worker

This is an implementation of an agent specialized in agent-to-agent communication and task coordination. The agent provides a standardized interface for processing messages and work requests between AI agents.

## Features

- Specialized in agent-to-agent communication
- Processes structured requests from other agents
- Maintains context across agent interactions
- Follows standard Evolve Agents Framework interface

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
docker build -t agent-worker .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 agent-worker
```

## Environment Variables

Required environment variables:
- AZURE_OPEN_AI_DEPLOYMENT_ID
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_MODEL
- AZURE_API_VERSION

## API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 