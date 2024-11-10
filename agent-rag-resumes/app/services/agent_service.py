from core.service_base import BaseAgentService
from app.core.agent import ResumeAgent

class ResumeAgentService(BaseAgentService):
    def __init__(self):
        super().__init__(ResumeAgent())
        self.initialize_agent()

    def initialize_agent(self):
        if isinstance(self.agent, ResumeAgent):
            self.agent.initialize_resume_index()

    def restart(self):
        self.agent = ResumeAgent()
        self.status = "idle"
        self.initialize_agent()
        return {"status": "success"} 