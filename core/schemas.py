from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class MessageHistory(BaseModel):
    role: str
    content: str

class Message(BaseModel):
    message: str
    role: str
    context: str
    history: List[MessageHistory]

class WorkRequest(BaseModel):
    task: str
    context: str
    history: List[MessageHistory]

class AgentResponse(BaseModel):
    status: str
    result: Optional[str] = None
    error: Optional[str] = None

class WorkStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkResult(BaseModel):
    work_id: str
    status: WorkStatus
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None 