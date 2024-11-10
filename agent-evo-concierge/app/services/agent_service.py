from core.service_base import BaseAgentService
from app.core.agent import ConciergeAgent

class ConciergeAgentService(BaseAgentService):
    def __init__(self):
        super().__init__(ConciergeAgent())

    def restart(self):
        self.agent = ConciergeAgent()
        self.status = "idle"
        return {"status": "success"} 