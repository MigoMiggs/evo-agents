from fastapi import APIRouter, HTTPException
from core.schemas import Message, WorkRequest, AgentResponse
from app.services.agent_service import ResumeAgentService

router = APIRouter()
agent_service = ResumeAgentService()

@router.post("/restart")
async def restart_agent():
    try:
        agent_service.restart()
        return {"status": "success", "message": "Agent restarted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/message", response_model=AgentResponse)
async def process_message(message: Message):
    try:
        return agent_service.process_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_status():
    try:
        return agent_service.get_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/work-request", response_model=AgentResponse)
async def process_work_request(work_request: WorkRequest):
    try:
        return agent_service.process_work_request(work_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 