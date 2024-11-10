from pydantic import BaseModel
from typing import List, Optional

class MessageHistory(BaseModel):
    role: str
    content: str

class Message(BaseModel):
    message: str
    role: str
    context: dict
    history: List[MessageHistory]

class WorkRequest(BaseModel):
    task: str
    context: dict
    history: List[MessageHistory]

class AgentResponse(BaseModel):
    status: str
    result: Optional[str] = None
    error: Optional[str] = None 