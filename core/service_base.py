from typing import Dict, Any, Optional
from core.schemas import Message, WorkRequest, AgentResponse, WorkResult
from core.agent_base import BaseAgent
import uuid
from datetime import datetime

class BaseAgentService:
    """Base service class for handling agent operations"""
    
    def __init__(self, agent: BaseAgent):
        self.agent = agent
        self.status = "idle"

    def restart(self) -> Dict[str, str]:
        """Restart the agent service"""
        self.status = "idle"
        return {"status": "success"}

    def process_message(self, message: Message) -> AgentResponse:
        """Process an incoming message"""
        try:
            self.status = "in_progress"
            result, response_memory = self.agent.process_message(
                message.message,
                message.role,
                message.context,
                message.history
            )
            self.status = "completed"
            return AgentResponse(status="completed", result=result, memory=response_memory)
        except Exception as e:
            self.status = "failed"
            return AgentResponse(status="failed", error=str(e))

    def get_status(self) -> Dict[str, str]:
        """Get current service status"""
        return {"status": self.status}

    async def process_work_request(self, work_request: WorkRequest) -> WorkResult:
        """Start an asynchronous work request"""
        try:
            return await self.agent.start_work(
                work_request.task,
                work_request.context,
                work_request.history
            )
        except Exception as e:
            return WorkResult(
                work_id=str(uuid.uuid4()),
                status="failed",
                error=str(e),
                created_at=datetime.utcnow(),
                completed_at=datetime.utcnow()
            )

    def get_work_result(self, work_id: str) -> Optional[WorkResult]:
        """Get the result of an async work request"""
        return self.agent.get_work_result(work_id) 