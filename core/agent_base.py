from typing import List, Optional
from abc import ABC, abstractmethod
from core.schemas import MessageHistory, AgentResponse
from llama_index.core import PromptTemplate
from llama_index.core.base.llms.types import ChatMessage    


class BaseAgent(ABC):
    """Base class for all agents in the framework"""

    TEMPLATE_TEXT = (
        "You are a helpful Evolve AI agent who is able to process messages or work requests. \n"
        "You are given context information below, the context includes information about the user, "
        "information helpful to complete the task and "
        "could contain additional instructions for you to do the work."
        "The context below is provided to help you complete the task."
        "----------------------------------\n "
        "{agent_internal_context}"
        "\n\n"
        "{agent_external_context}"
        "----------------------------------\n"
    )
    
    AGENT_SYS_PROMPT_TEMPLATE = PromptTemplate(TEMPLATE_TEXT)

    
    def __init__(self):
        self.state = "initialized"

    # function that turns a lits of MessageHistory to a list of ChatMessage
    def history_to_chat_messages(self, history: List[MessageHistory]) -> List[ChatMessage]:
        return [ChatMessage(role=m.role, content=m.content) for m in history]
        
    @abstractmethod
    def process_message(
        self,
        message: str,
        role: str,
        context: str,
        history: List[MessageHistory]
    ) -> str:
        """Process an incoming message"""
        pass
        
    @abstractmethod
    def process_work_request(
        self,
        task: str,
        context: str,
        history: List[MessageHistory]
    ) -> str:
        """Process a work request"""
        pass
        
    def get_state(self) -> str:
        """Get current agent state"""
        return self.state 