from typing import List
from core.agent_base import BaseAgent
from core.schemas import MessageHistory
from llama_index.agent.openai import OpenAIAgent
from core.azure_llm import AzureLLM
import os
from llama_index.core import Settings
from dotenv import load_dotenv

load_dotenv()
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

        self.agent = OpenAIAgent.from_tools(    
            llm=self.llm.llm
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
        response = self.agent.chat(message)
        return response.response

    def process_work_request(
        self,
        task: str,
        context: dict,
        history: List[MessageHistory]
    ) -> str:
        # Concierge-specific task processing implementation
        return f"Processed concierge task: {task}" 