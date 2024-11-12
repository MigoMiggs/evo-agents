from typing import List, Tuple
from core.agent_base import BaseAgent
from core.schemas import MessageHistory
from core.schemas import WorkAgentToAgent
from core.client.http import HttpAgentClient
from core.schemas import Message
from llama_index.agent.openai import OpenAIAgent
from core.azure_openai_llm import AzureOpenAILLM
from llama_index.core.prompts.base import PromptTemplate
import os
from llama_index.core import Settings
from llama_index.core.base.llms.types import ChatMessage
from core.schemas import TargetAgentEnum
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

    WORK_AGENT_TO_AGENT_PROMPT = (
        "You are an AI agent worker specialized in communicating with other AI agents. "
        "You will be given a structure to populate that will give us the initial message "
        "and context for a conversation with another agent. "
        "Your job is to construct the initial message to send to the other agent. "
        "Make sure the initial message represents the task you are trying to complete. Make it actionable."
        "You will figure out the maximum number of turns this conversation should have, try the least number of turns possible. "
        "You will also figure out which agent you are going to send the message to. "
        "Take the task below and user that get the information you need to populate the structure. "
        "----------------------------------\n "
        "{task}"
        "----------------------------------\n "
    )
    
    WORK_AGENT_TO_AGENT_PROMPT_TEMPLATE = PromptTemplate(WORK_AGENT_TO_AGENT_PROMPT)

    WORK_AGENT_NEXT_MESSAGE_PROMPT = (
        "Pretend you are a user of the concierge agent. "
        "You will be given the chat history and the last message sent to you by the concierge agent. "
        "Dont say anything inappropriate."
        "Use that information to predict the next message. "
        "Return the next message only, nothing else. "
        "----------------------------------\n "
        "{chat_history}"
        "----------------------------------\n "
    )

    WORK_AGENT_NEXT_MESSAGE_PROMPT_TEMPLATE = PromptTemplate(WORK_AGENT_NEXT_MESSAGE_PROMPT)

    WORK_AGENT_CONVERSATION_COMPLETE_PROMPT = (
        "The conversation is complete. "
        "Return the final message only, nothing else. "
        "Take the whole chat history and turn it into a single message that captures the whole conversation. "
        "----------------------------------\n "
        "{chat_history}"
        "----------------------------------\n " 
    )

    WORK_AGENT_CONVERSATION_COMPLETE_PROMPT_TEMPLATE = PromptTemplate(WORK_AGENT_CONVERSATION_COMPLETE_PROMPT)

    def __init__(self):
        self.llm = AzureOpenAILLM(
            model_config={
                "deployment_name": os.getenv("AZURE_OPEN_AI_DEPLOYMENT_ID"),
                "api_base": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                "model": os.getenv("AZURE_OPENAI_MODEL"),
                "api_version": os.getenv("AZURE_API_VERSION"),
                "temperature": .5
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

        # Create new message history entries
        new_message = MessageHistory(role=role, content=response.response)
        agent_response = MessageHistory(role="assistant", content=response.response)
        
        # Return both response and updated history
        response_memory = history + [new_message, agent_response]
        return response.response, response_memory

    async def process_work_request(
        self,
        task: str,
        context: str,
        history: List[MessageHistory]
    ) -> Tuple[str, List[MessageHistory]]:
        sys_prompt = self.AGENT_SYS_PROMPT_TEMPLATE.format(
            agent_internal_context=self.INTERNAL_CONTEXT,
            agent_external_context=context
        )

        if history is None:
            chat_history = []    
        else:
            chat_history = self.history_to_chat_messages(history)

        # Get the work agent to agent configuration
        work_agent_to_agent = self._get_work_agent_to_agent_config(task)
        result, updated_history = await self._work_agent_to_agent(work_agent_to_agent)
        return result, updated_history
    
    def _get_work_agent_to_agent_config(self, task: str) -> WorkAgentToAgent:
        sllm = self.llm.llm.as_structured_llm(output_cls=WorkAgentToAgent)
        prompt = self.WORK_AGENT_TO_AGENT_PROMPT_TEMPLATE.format(task=task)
        message = ChatMessage.from_str(prompt)
        response = sllm.chat([message])

        return response.raw
    
    async def _work_agent_to_agent(self, work_agent_to_agent: WorkAgentToAgent) -> tuple[str, List[MessageHistory]]:

        number_of_turns = work_agent_to_agent.max_turns

        #figure out the agent to send the message to, and if its not the concierge,
        # throw an error saying that the agent is not supported
        if work_agent_to_agent.target_agent_id != TargetAgentEnum.AGENT_CONCIERGE:
            raise ValueError(f"Agent {work_agent_to_agent.target_agent_id} is not supported")
        
        agent_concierge_base_url = os.getenv("AGENT_CONCIERGE_BASE_URL")
        number_of_turns = work_agent_to_agent.max_turns

        target_agent_chat_history = []

        #create new Message for the concierge
        message = Message(
            message=work_agent_to_agent.initial_message.message,
            role="user",
            context=work_agent_to_agent.initial_context,
            history=target_agent_chat_history
        )

        while number_of_turns > 0:
            async with HttpAgentClient(agent_concierge_base_url) as client:
                
                try:        
                    # Send message and get response
                    print(f"Sending message to concierge: {message.message}")
                    response = await client.process_message(message)

                    if response.status == "completed":
                        target_agent_chat_history = response.memory
                    else:
                        print(f"Error communicating with agent: {response.error}")
                        break

                    print(f"Received message from concierge: {response.result}")

                    # Get the next message
                    messages = self.history_to_chat_messages(target_agent_chat_history)
                    history_str = "\n".join([f"{m.role}: {m.content}" for m in messages])
                    prompt = self.WORK_AGENT_NEXT_MESSAGE_PROMPT_TEMPLATE.format(chat_history=history_str)

                    # convert prompt to ChatMessage
                    prompt = ChatMessage.from_str(prompt)
                    next_message = self.llm.llm.chat([prompt])

                    #next_message = await self.llm.generate(prompt=prompt, temperature=.5)

                    message.message = next_message.message.content
                    message.history = response.memory

                    if message.message == "":
                        # if the message is empty, agent has exhusted what it can do
                        break

                except Exception as e:
                    print(f"Error communicating with agent: {str(e)}")
                    break

                number_of_turns -= 1

        # synthesize the final message
        messages = self.history_to_chat_messages(target_agent_chat_history)
        history_str = "\n".join([f"{m.role}: {m.content}" for m in messages])
        prompt = self.WORK_AGENT_CONVERSATION_COMPLETE_PROMPT_TEMPLATE.format(chat_history=history_str)
        prompt = ChatMessage.from_str(prompt)
        final_message = self.llm.llm.chat([prompt])

        final_message_content = final_message.message.content

        return final_message_content, target_agent_chat_history

    