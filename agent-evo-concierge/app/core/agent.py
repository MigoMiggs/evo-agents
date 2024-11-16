from typing import List, Tuple
from core.agent_base import BaseAgent
from core.schemas import MessageHistory, WorkRequestFile
from llama_index.agent.openai import OpenAIAgent
from core.azure_openai_llm import AzureOpenAILLM
import os
from llama_index.core import Settings
from dotenv import load_dotenv
import logging

# Get logger
logger = logging.getLogger("evo_concierge")

load_dotenv()

class ConciergeAgent(BaseAgent):
    def __init__(self):
        logger.info("Initializing ConciergeAgent")
        self.llm = AzureOpenAILLM(
            model_config={
                "deployment_name": os.getenv("AZURE_OPEN_AI_DEPLOYMENT_ID"),
                "api_base": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                "model": os.getenv("AZURE_OPENAI_MODEL"),
                "api_version": os.getenv("AZURE_API_VERSION")
            }
        )
        logger.debug("LLM initialized successfully")
        super().__init__()

    def process_message(
        self,
        message: str,
        role: str,
        context: str,
        history: List[MessageHistory]
    ) -> Tuple[str, List[MessageHistory]]:
        logger.info(f"Processing message from role: {role}")
        logger.debug(f"Message content: {message}")
        logger.debug(f"Context: {context}")
        
        # Rest of your implementation...

    async def process_work_request(
        self,
        task: str,
        context: str,
        history: List[MessageHistory]
    ) -> Tuple[str, List[MessageHistory]]:
        # Concierge-specific task processing implementation
        result = f"Processed concierge task: {task}"
        
        # Create new history entries
        task_message = MessageHistory(role="user", content=task)
        response_message = MessageHistory(role="assistant", content=result)
        updated_history = history + [task_message, response_message]
        
        return result, updated_history

    async def process_work_request_with_file(
        self,
        task: str,
        context: str,
        history: List[MessageHistory],
        file: WorkRequestFile
    ) -> Tuple[str, List[MessageHistory]]:
        """Process work request with file"""
        # For Concierge, we'll just acknowledge the file
        enhanced_context = f"{context}\n\nFile received: {file.filename}"
        return await self.process_work_request(task, enhanced_context, history)