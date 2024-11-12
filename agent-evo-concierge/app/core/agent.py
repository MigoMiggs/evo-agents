from typing import List, Tuple
from core.agent_base import BaseAgent
from core.schemas import MessageHistory
from llama_index.agent.openai import OpenAIAgent
from core.azure_openai_llm import AzureOpenAILLM
import os
from llama_index.core import Settings
from dotenv import load_dotenv

load_dotenv()
class ConciergeAgent(BaseAgent):
    
    agent = None

    INTERNAL_CONTEXT = ("Your name is Evo the Concierge. \n"
                        "You can help the user navigate through the Evolve system."
    )

    def __init__(self):
        self.llm = AzureOpenAILLM(
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
    ) -> Tuple[str, List[MessageHistory]]:
        # Concierge-specific message processing implementation

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

        print(sys_prompt)
        response = self.agent.chat(message)
        response_memory = self.agent.memory.get_all()

        # convert response memory to list of MessageHistory objects
        response_memory = [MessageHistory(role=m.role, content=m.content) for m in response_memory]
        return response.response, response_memory

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