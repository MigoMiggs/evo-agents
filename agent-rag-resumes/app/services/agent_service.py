from app.models.schemas import Message, WorkRequest, AgentResponse
from app.core.agent import Agent

class AgentService:
    def __init__(self):
        self.agent = Agent()
        self.status = "idle"
        self.initialize_agent()

    def initialize_agent(self):
        self.agent.initialize_resume_index()

    def restart(self):
        self.agent = Agent()
        self.status = "idle"
        self.initialize_agent()
        return {"status": "success"}

    def process_message(self, message: Message) -> AgentResponse:
        try:
            self.status = "in_progress"
            result = self.agent.process_message(
                message.message,
                message.role,
                message.context,
                message.history
            )
            self.status = "completed"
            return AgentResponse(status="completed", result=result)
        except Exception as e:
            self.status = "failed"
            return AgentResponse(status="failed", error=str(e))

    def get_status(self):
        return {"status": self.status}

    def process_work_request(self, work_request: WorkRequest) -> AgentResponse:
        try:
            self.status = "in_progress"
            result = self.agent.process_work_request(
                work_request.task,
                work_request.context,
                work_request.history
            )
            self.status = "completed"
            return AgentResponse(status="completed", result=result)
        except Exception as e:
            self.status = "failed"
            return AgentResponse(status="failed", error=str(e)) 