from fastapi import APIRouter, HTTPException
from core.schemas import Message, WorkRequest, AgentResponse, WorkResult
from app.services.agent_service import AgentWorkerService

router = APIRouter()
agent_service = AgentWorkerService()

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

@router.post("/work-request", response_model=WorkResult)
async def process_work_request(work_request: WorkRequest):
    try:
        return await agent_service.process_work_request(work_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/work-result/{work_id}", response_model=WorkResult)
async def get_work_result(work_id: str):
    try:
        result = agent_service.get_work_result(work_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Work request not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 