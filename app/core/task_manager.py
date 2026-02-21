"""
任务管理器
"""
import os
import uuid
import threading
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional, Callable
from datetime import datetime

from app.models.task import TaskType, TaskStatus

logger = logging.getLogger(__name__)


class Task:
    def __init__(
        self,
        task_id: str,
        task_type: TaskType,
        devices: list,
        ai_type: str,
        handler: Optional[Callable] = None,
    ):
        self.task_id = task_id
        self.task_type = task_type
        self.devices = devices
        self.ai_type = ai_type
        self.handler = handler
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
            self._tasks_lock = threading.Lock()
            max_workers = max(2, min(8, os.cpu_count() or 4))
            self._max_pending = max(10, int(os.getenv("MYT_TASK_MAX_PENDING", "200")))
            self._pending_submissions = 0
            self._executor = ThreadPoolExecutor(
                max_workers=max_workers,
                thread_name_prefix="task-worker",
            )
            self._max_workers = max_workers
            self._initialized = True

    def create_task(
        self,
        task_type: TaskType,
        devices: list,
        ai_type: str,
        handler: Optional[Callable] = None,
    ) -> Task:
        task_id = str(uuid.uuid4())[:8]
        task = Task(task_id, task_type, devices, ai_type, handler=handler)
        with self._tasks_lock:
            self._tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        with self._tasks_lock:
            return self._tasks.get(task_id)

    def get_all_tasks(self) -> list:
        with self._tasks_lock:
            return list(self._tasks.values())

    def set_task_handler(self, task_id: str, handler: Callable) -> bool:
        with self._tasks_lock:
            task = self._tasks.get(task_id)
            if not task:
                return False
            task.handler = handler
            return True

    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Optional[dict] = None,
        error: Optional[str] = None,
    ):
        with self._tasks_lock:
            task = self._tasks.get(task_id)
            if not task:
                return
            task.status = status
            if result is not None:
                task.result = result
            if error is not None:
                task.error = error
            if status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                task.completed_at = datetime.now()

    def _resolve_handler(self, task: Task) -> Optional[Callable]:
        return task.handler

    def _execute_task(self, task_id: str):
        task = self.get_task(task_id)
        if not task:
            return

        handler = self._resolve_handler(task)
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

    def _execute_and_finalize(self, task_id: str):
        try:
            self._execute_task(task_id)
        finally:
            with self._tasks_lock:
                if self._pending_submissions > 0:
                    self._pending_submissions -= 1

    def run_task_async(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False

        queue_full = False
        with self._tasks_lock:
            if self._pending_submissions >= self._max_pending:
                queue_full = True
            else:
                self._pending_submissions += 1

        if queue_full:
            self.update_task_status(task_id, TaskStatus.FAILED, error="Task queue is full")
            return False

        self._executor.submit(self._execute_and_finalize, task_id)
        return True

    def get_runtime_stats(self) -> dict:
        with self._tasks_lock:
            tasks = list(self._tasks.values())
            counts = {
                "pending": 0,
                "running": 0,
                "completed": 0,
                "failed": 0,
                "cancelled": 0,
            }
            for t in tasks:
                key = t.status.value
                if key in counts:
                    counts[key] += 1

            return {
                "workers": self._max_workers,
                "pending_submissions": self._pending_submissions,
                "max_pending": self._max_pending,
                "task_total": len(tasks),
                **counts,
            }
