from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class TaskType(str, Enum):
    FULL_FLOW = "full_flow"
    NURTURE_FLOW = "nurture_flow"
    RESET_LOGIN = "reset_login"
    SINGLE_TASK = "single_task"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskRequest(BaseModel):
    devices: List[int]
    ai_type: str = "volc"


class TaskResponse(BaseModel):
    task_id: str
    task_type: TaskType
    devices: List[int]
    ai_type: str
    status: TaskStatus
    created_at: datetime


class TaskDetailResponse(TaskResponse):
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
