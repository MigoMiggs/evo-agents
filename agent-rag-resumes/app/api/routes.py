from fastapi import APIRouter, HTTPException
from core.schemas import Message, WorkRequest, AgentResponse
from app.services.agent_service import ResumeAgentService

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