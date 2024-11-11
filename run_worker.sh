#!/bin/bash

# Export environment variables from .env file
export $(cat .env | xargs)

# Start the FastAPI application using uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 