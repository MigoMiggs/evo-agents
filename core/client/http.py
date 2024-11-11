from typing import Dict, Any, Optional
import aiohttp
from urllib.parse import urljoin
from .base import BaseAgentClient
from ..schemas import Message, WorkRequest, AgentResponse

class HttpAgentClient(BaseAgentClient):
    """HTTP client implementation for interacting with agent services"""
    
    def __init__(self, base_url: str):
        """Initialize with base URL of the agent service"""
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    def _get_url(self, endpoint: str) -> str:
        """Construct full URL for given endpoint"""
        return urljoin(f"{self.base_url}/", endpoint.lstrip('/'))
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def restart(self) -> Dict[str, Any]:
        """Restart the agent"""
        await self._ensure_session()
        async with self.session.post(self._get_url('/agent/restart')) as response:
            response.raise_for_status()
            return await response.json()
            
    async def process_message(self, message: Message) -> AgentResponse:
        """Send a message to the agent"""
        await self._ensure_session()
        async with self.session.post(
            self._get_url('/agent/message'),
            json=message.model_dump()
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return AgentResponse(**data)
            
    async def get_status(self) -> Dict[str, str]:
        """Get the agent's current status"""
        await self._ensure_session()
        async with self.session.get(self._get_url('/agent/status')) as response:
            response.raise_for_status()
            return await response.json()
            
    async def process_work_request(self, work_request: WorkRequest) -> AgentResponse:
        """Send a work request to the agent"""
        await self._ensure_session()
        async with self.session.post(
            self._get_url('/agent/work-request'),
            json=work_request.model_dump()
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return AgentResponse(**data) 