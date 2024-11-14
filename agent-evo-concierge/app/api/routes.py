from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from core.schemas import Message, WorkRequest, AgentResponse, WorkRequestFile, WorkResult
from app.services.agent_service import ConciergeAgentService
import shutil
from pathlib import Path
from fastapi import Body

# At the top of your file, after creating the FastAPI app
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
agent_service = ConciergeAgentService()

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

        work_request = WorkRequest()
            
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

@router.get("/work-result/{work_id}", response_model=WorkResult)
async def get_work_result(work_id: str):
    """
    Get the result of an async work request.
    
    Takes a work_id and returns the WorkResult with status and optional result/error.
    """
    try:
        result = agent_service.get_work_result(work_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Work request not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

