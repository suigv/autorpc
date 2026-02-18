"""
任务管理器
"""
import uuid
import threading
import logging
from typing import Dict, Optional, Callable
from datetime import datetime
from enum import Enum

from app.models.task import TaskType, TaskStatus

logger = logging.getLogger(__name__)


class Task:
    def __init__(self, task_id: str, task_type: TaskType, devices: list, ai_type: str):
        self.task_id = task_id
        self.task_type = task_type
        self.devices = devices
        self.ai_type = ai_type
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.result: Optional[dict] = None
        self.error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "devices": self.devices,
            "ai_type": self.ai_type,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error
        }


class TaskManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._tasks: Dict[str, Task] = {}
            self._task_handlers: Dict[TaskType, Callable] = {}
            self._initialized = True

    def register_handler(self, task_type: TaskType, handler: Callable):
        self._task_handlers[task_type] = handler

    def create_task(self, task_type: TaskType, devices: list, ai_type: str) -> Task:
        task_id = str(uuid.uuid4())[:8]
        task = Task(task_id, task_type, devices, ai_type)
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list:
        return list(self._tasks.values())

    def update_task_status(self, task_id: str, status: TaskStatus, result: dict = None, error: str = None):
        task = self._tasks.get(task_id)
        if task:
            task.status = status
            if result:
                task.result = result
            if error:
                task.error = error
            if status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                task.completed_at = datetime.now()

    def run_task_async(self, task_id: str):
        task = self._tasks.get(task_id)
        if not task:
            return

        def execute():
            handler = self._task_handlers.get(task.task_type)
            if not handler:
                self.update_task_status(task_id, TaskStatus.FAILED, error="No handler registered")
                return

            try:
                self.update_task_status(task_id, TaskStatus.RUNNING)
                result = handler(task.devices, task.ai_type)
                self.update_task_status(task_id, TaskStatus.COMPLETED, result=result)
            except Exception as e:
                logger.exception(f"Task {task_id} failed")
                self.update_task_status(task_id, TaskStatus.FAILED, error=str(e))

        thread = threading.Thread(target=execute)
        thread.start()
