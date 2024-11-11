from typing import List
from core.agent_base import BaseAgent
from core.schemas import MessageHistory
from llama_index.agent.openai import OpenAIAgent
from core.azure_llm import AzureLLM
import os
from llama_index.core import Settings
from dotenv import load_dotenv
import asyncio

load_dotenv()

class AgentWorker(BaseAgent):
    
    agent = None

    INTERNAL_CONTEXT = (
        "You are an AI agent worker specialized in communicating with other AI agents. "
        "You can understand and process requests from other agents, coordinate work, "
        "and provide structured responses that other agents can easily interpret. "
        "You maintain professional and efficient communication with other AI agents."
    )

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
        context: str,
        history: List[MessageHistory]
    ) -> str:
        sys_prompt = self.AGENT_SYS_PROMPT_TEMPLATE.format(
            agent_internal_context=self.INTERNAL_CONTEXT,
            agent_external_context=context
        )

        chat_history = self.history_to_chat_messages(history)

        self.agent = OpenAIAgent.from_tools(    
            llm=self.llm.llm,
            system_prompt=sys_prompt, 
            chat_history=chat_history
        )

        response = self.agent.chat(message)
        return response.response

    async def process_work_request(
        self,
        task: str,
        context: str,
        history: List[MessageHistory]
    ) -> str:
        sys_prompt = self.AGENT_SYS_PROMPT_TEMPLATE.format(
            agent_internal_context=self.INTERNAL_CONTEXT,
            agent_external_context=context
        )

        chat_history = self.history_to_chat_messages(history)

        self.agent = OpenAIAgent.from_tools(    
            llm=self.llm.llm,
            system_prompt=sys_prompt, 
            chat_history=chat_history
        )

        # Simulate async work
        await asyncio.sleep(1)  # Replace with actual async work
        response = self.agent.chat(f"Please process this task: {task}")
        return response.response 