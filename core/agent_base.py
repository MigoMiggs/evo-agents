from typing import List, Optional
from abc import ABC, abstractmethod
from core.schemas import MessageHistory, AgentResponse

class BaseAgent(ABC):
    """Base class for all agents in the framework"""
    
    def __init__(self):
        self.state = "initialized"
        
    @abstractmethod
    def process_message(
        self,
        message: str,
        role: str,
        context: dict,
        history: List[MessageHistory]
    ) -> str:
        """Process an incoming message"""
        pass
        
    @abstractmethod
    def process_work_request(
        self,
        task: str,
        context: dict,
        history: List[MessageHistory]
    ) -> str:
        """Process a work request"""
        pass
        
    def get_state(self) -> str:
        """Get current agent state"""
        return self.state 