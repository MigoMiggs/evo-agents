from typing import List
from app.models.schemas import MessageHistory

class Agent:
    def __init__(self):
        self.state = "initialized"

    def process_message(
        self,
        message: str,
        role: str,
        context: dict,
        history: List[MessageHistory]
    ) -> str:
        # Implement your agent's message processing logic here
        return f"Processed message: {message}"

    def process_work_request(
        self,
        task: str,
        context: dict,
        history: List[MessageHistory]
    ) -> str:
        # Implement your agent's work request processing logic here
        return f"Processed task: {task}" 