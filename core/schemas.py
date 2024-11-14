from pydantic import BaseModel
from typing import List, Optional, Dict, Any, BinaryIO
from enum import Enum
from datetime import datetime

class MessageHistory(BaseModel):
    role: str
    content: str

class Message(BaseModel):
    message: str
    role: str
    context: str
    history: Optional[List[MessageHistory]] = None

class WorkRequestFile(BaseModel):
    filename: str
    content_type: str
    file_path: str  # Path where file is stored locally

class WorkRequest(BaseModel):
    task: str = "task"
    context: str = "context"
    history: Optional[List[MessageHistory]] = []  
    file: Optional[WorkRequestFile] = None  # Add file information

class AgentResponse(BaseModel):
    status: str
    result: Optional[str] = None
    error: Optional[str] = None
    memory: Optional[List[MessageHistory]] = []

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
    memory: Optional[List[MessageHistory]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    file_path: Optional[str] = None  # Add reference to processed file

class TargetAgentEnum(str, Enum):
    AGENT_CONCIERGE = "AGENT_CONCIERGE"

class WorkAgentToAgent(BaseModel):
    target_agent_id: TargetAgentEnum
    initial_message: Message
    initial_context: str
    max_turns: int = 10
    