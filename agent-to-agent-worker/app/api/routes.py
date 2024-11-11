from fastapi import APIRouter, HTTPException
from core.schemas import Message, WorkRequest, AgentResponse, WorkResult
from app.services.agent_service import AgentWorkerService

router = APIRouter()
agent_service = AgentWorkerService()

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

@router.post("/work-request", response_model=WorkResult)
async def process_work_request(
    work_request: WorkRequest = WorkRequest(
        task="Get the Concierge Aagent to have a friendly conversation and stop when feel it has been cordial.",
        context="Example context information",
        history=[
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hello"}
        ]
    )):
    """
    Process an asynchronous work request for the agent.
    
    Takes a WorkRequest containing the task, context and history.
    Returns a WorkResult with status and optional result/error.
    """
    try:
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