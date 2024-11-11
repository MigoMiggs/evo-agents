from core.service_base import BaseAgentService
from app.core.agent import AgentWorker

class AgentWorkerService(BaseAgentService):
    def __init__(self):
        super().__init__(AgentWorker())

    def restart(self):
        self.agent = AgentWorker()
        self.status = "idle"
        return {"status": "success"} 