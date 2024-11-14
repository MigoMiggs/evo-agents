from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from core.schemas import Message, WorkRequest, AgentResponse, WorkRequestFile, WorkResult
from app.services.agent_service import ResumeAgentService
import shutil
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

router = APIRouter()
agent_service = ResumeAgentService()

@router.post("/restart")
async def restart_agent():
    """
    Restart the agent.
    
    Returns a success message if the agent is restarted successfully.
    """
    try:
        agent_service.restart()
        return {"status": "success", "message": "Agent restarted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/message", response_model=AgentResponse)
async def process_message(message: Message):
    """
    Process a message for the agent.
    
    Takes a Message containing the role, context and history.
    Returns an AgentResponse with status and optional result/error.
    """
    try:
        return agent_service.process_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_status():
    """
    Get the current status of the agent.
    
    Returns a dictionary with the status of the agent.
    """
    try:
        return agent_service.get_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/work-request", response_model=AgentResponse)
async def process_work_request(work_request: WorkRequest):
    """
    Process an asynchronous work request for the agent.
    
    Takes a WorkRequest containing the task, context and history.
    Returns an AgentResponse with status and optional result/error.
    """
    try:
        return agent_service.process_work_request(work_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/work-request-with-file", response_model=WorkResult)
async def process_work_request_with_file(
    work_request: WorkRequest,
    file: UploadFile = File(...)
):
    """Process work request with file upload"""
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Save uploaded file
        file_path = upload_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Create WorkRequestFile
        work_file = WorkRequestFile(
            filename=file.filename,
            content_type=file.content_type,
            file_path=str(file_path)
        )
        
        # Add file to work request
        work_request.file = work_file
        
        return await agent_service.process_work_request(work_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 