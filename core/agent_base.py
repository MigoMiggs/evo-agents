from typing import List, Optional
from abc import ABC, abstractmethod
from core.schemas import MessageHistory, AgentResponse
from llama_index.core import PromptTemplate

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

    def display_prompt_dict(prompts_dict):
        for k, p in prompts_dict.items():
            text_md = f"**Prompt Key**: {k}<br>" f"**Text:** <br>"
            print(text_md)
            print(p.get_template())
            print("<br><br>")
        
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