from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class MessageHistory(BaseModel):
    role: str
    content: str

class Message(BaseModel):
    message: str
    role: str
    context: Dict[str, Any]
    history: List[MessageHistory]

class WorkRequest(BaseModel):
    task: str
    context: Dict[str, Any]
    history: List[MessageHistory]

class AgentResponse(BaseModel):
    status: str
    result: Optional[str] = None
    error: Optional[str] = None 