from typing import Dict, Any
from core.schemas import Message, WorkRequest, AgentResponse
from core.agent_base import BaseAgent

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
            result = self.agent.process_message(
                message.message,
                message.role,
                message.context,
                message.history
            )
            self.status = "completed"
            return AgentResponse(status="completed", result=result)
        except Exception as e:
            self.status = "failed"
            return AgentResponse(status="failed", error=str(e))

    def get_status(self) -> Dict[str, str]:
        """Get current service status"""
        return {"status": self.status}

    def process_work_request(self, work_request: WorkRequest) -> AgentResponse:
        """Process a work request"""
        try:
            self.status = "in_progress"
            result = self.agent.process_work_request(
                work_request.task,
                work_request.context,
                work_request.history
            )
            self.status = "completed"
            return AgentResponse(status="completed", result=result)
        except Exception as e:
            self.status = "failed"
            return AgentResponse(status="failed", error=str(e)) 