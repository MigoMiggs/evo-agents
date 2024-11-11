from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..schemas import Message, WorkRequest, AgentResponse

class BaseAgentClient(ABC):
    """Abstract base class for agent clients"""
    
    @abstractmethod
    async def restart(self) -> Dict[str, Any]:
        """Restart the agent"""
        pass
        
    @abstractmethod
    async def process_message(self, message: Message) -> AgentResponse:
        """Send a message to the agent"""
        pass
        
    @abstractmethod
    async def get_status(self) -> Dict[str, str]:
        """Get the agent's current status"""
        pass
        
    @abstractmethod
    async def process_work_request(self, work_request: WorkRequest) -> AgentResponse:
        """Send a work request to the agent"""
        pass 