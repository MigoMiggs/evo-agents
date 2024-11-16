from core.service_base import BaseAgentService
from app.core.agent import ConciergeAgent
from core.schemas import Message, AgentResponse
import logging

logger = logging.getLogger("evo_concierge")

class ConciergeAgentService(BaseAgentService):
    def __init__(self):
        super().__init__(ConciergeAgent())

    def restart(self):
        self.agent = ConciergeAgent()
        self.status = "idle"
        return {"status": "success"}

    def process_message_for_file(self, message: Message) -> AgentResponse:
        """
        Concierge-specific implementation for processing file-based messages.
        This method can be customized to handle file content in a way specific to the concierge agent.
        """
        try:
            logger.info("Processing file-based message in ConciergeAgent")
            logger.debug(f"Message: {message.message}")
            logger.debug(f"Context length: {len(message.context)}")

            # You could add specific file-handling logic here
            # For example, you might want to format the context differently
            # or add specific instructions for file-related queries
            
            enhanced_context = (
                "You are analyzing a file's contents. "
                "Please provide specific and relevant information from the file "
                "in response to the user's query.\n\n"
                f"{message.context}"
            )
            
            # Create a new message with enhanced context
            enhanced_message = Message(
                message=message.message,
                role=message.role,
                context=enhanced_context,
                history=message.history
            )
            
            # Process the enhanced message
            result, memory = self.agent.process_message(
                enhanced_message.message,
                enhanced_message.role,
                enhanced_message.context,
                enhanced_message.history or []
            )
            
            return AgentResponse(status="completed", result=result, memory=memory)
            
        except Exception as e:
            logger.error(f"Error in ConciergeAgent processing file message: {str(e)}", exc_info=True)
            return AgentResponse(status="error", error=str(e)) 