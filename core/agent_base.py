from typing import List, Optional, Dict
from abc import ABC, abstractmethod
from core.schemas import MessageHistory, AgentResponse, WorkResult, WorkStatus
from llama_index.core import PromptTemplate
from llama_index.core.base.llms.types import ChatMessage
from datetime import datetime
import uuid
import asyncio

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
        self.work_items: Dict[str, WorkResult] = {}

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
    async def process_work_request(
        self,
        task: str,
        context: str,
        history: List[MessageHistory]
    ) -> str:
        """Process a work request asynchronously"""
        pass

    async def start_work(
        self,
        task: str,
        context: str,
        history: List[MessageHistory]
    ) -> WorkResult:
        """Start an asynchronous work request"""
        work_id = str(uuid.uuid4())
        
        # Create work result entry
        work_result = WorkResult(
            work_id=work_id,
            status=WorkStatus.PENDING,
            created_at=datetime.utcnow()
        )
        self.work_items[work_id] = work_result

        # Start work in background
        asyncio.create_task(self._execute_work(work_id, task, context, history))
        
        return work_result

    async def _execute_work(
        self,
        work_id: str,
        task: str,
        context: str,
        history: List[MessageHistory]
    ):
        """Execute the work request and update status"""
        work_result = self.work_items[work_id]
        work_result.status = WorkStatus.IN_PROGRESS
        
        try:
            result = await self.process_work_request(task, context, history)
            work_result.status = WorkStatus.COMPLETED
            work_result.result = result
        except Exception as e:
            work_result.status = WorkStatus.FAILED
            work_result.error = str(e)
        
        work_result.completed_at = datetime.utcnow()
        
    def get_work_result(self, work_id: str) -> Optional[WorkResult]:
        """Get the result of an async work request"""
        return self.work_items.get(work_id)
        
    def get_state(self) -> str:
        """Get current agent state"""
        return self.state