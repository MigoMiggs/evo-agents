from typing import List
from core.agent_base import BaseAgent
from core.schemas import MessageHistory
from core.azure_llm import AzureLLM
import os
class ConciergeAgent(BaseAgent):


    def __init__(self):
        self.llm = AzureLLM(
            model_config={
                "deployment_name": os.getenv("AZURE_OPEN_AI_DEPLOYMENT_ID"),
                "api_base": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                "model": os.getenv("AZURE_OPENAI_MODEL"),
                "api_version": os.getenv("AZURE_API_VERSION")
            }
        )

        super().__init__()

    def process_message(
        self,
        message: str,
        role: str,
        context: dict,
        history: List[MessageHistory]
    ) -> str:
        # Concierge-specific message processing implementation
        return f"Processed concierge message: {message}"

    def process_work_request(
        self,
        task: str,
        context: dict,
        history: List[MessageHistory]
    ) -> str:
        # Concierge-specific task processing implementation
        return f"Processed concierge task: {task}" 