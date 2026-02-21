"""
任务 API
"""
from fastapi import APIRouter, HTTPException
from typing import Callable, List, Optional

from app.models.task import TaskRequest, TaskResponse, TaskDetailResponse, TaskType, TaskStatus
from app.core.workflow_engine import WorkflowEngine
from app.core.device_manager import parse_ai_type
from app.core.task_manager import TaskManager
from app.core.task_log_store import get_task_logs
from common.runtime_state import reset_runtime_state

router = APIRouter()
workflow_engine = WorkflowEngine()
task_manager = TaskManager()


@router.post("/full-flow", response_model=TaskResponse)
def create_full_flow_task(request: TaskRequest):
    return _create_and_start_task(
        task_type=TaskType.FULL_FLOW,
        devices=request.devices,
        ai_type=parse_ai_type(request.ai_type),
        runner=workflow_engine.run_full_flow,
    )


@router.post("/nurture-flow", response_model=TaskResponse)
def create_nurture_flow_task(request: TaskRequest):
    return _create_and_start_task(
        task_type=TaskType.NURTURE_FLOW,
        devices=request.devices,
        ai_type=parse_ai_type(request.ai_type),
        runner=workflow_engine.run_nurture_flow,
    )


@router.post("/reset-login", response_model=TaskResponse)
def create_reset_login_task(request: TaskRequest):
    return _create_and_start_task(
        task_type=TaskType.RESET_LOGIN,
        devices=request.devices,
        ai_type=parse_ai_type(request.ai_type),
        runner=workflow_engine.run_reset_login,
    )


@router.get("/", response_model=List[TaskResponse])
def list_tasks(limit: int = 50):
    tasks = task_manager.get_all_tasks()
    tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)[:limit]
    return [
        TaskResponse(
            task_id=t.task_id,
            task_type=t.task_type,
            devices=t.devices,
            ai_type=t.ai_type,
            status=t.status,
            created_at=t.created_at
        )
        for t in tasks
    ]


@router.get("/logs")
def list_task_logs(
    device_index: Optional[int] = None,
    task_id: Optional[str] = None,
    since_id: int = 0,
    limit: int = 200,
):
    result = get_task_logs(
        device_index=device_index,
        task_id=task_id,
        since_id=since_id,
        limit=limit,
    )
    return {"status": "ok", **result}


@router.post("/initialize")
def initialize_runtime_state():
    workflow_engine.stop_all()
    reset_result = reset_runtime_state()
    return {"status": "ok", "message": "运行状态已初始化", **reset_result}


@router.get("/{task_id}", response_model=TaskDetailResponse)
def get_task(task_id: str):
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskDetailResponse(
        task_id=task.task_id,
        task_type=task.task_type,
        devices=task.devices,
        ai_type=task.ai_type,
        status=task.status,
        created_at=task.created_at,
        result=task.result,
        error=task.error
    )


@router.post("/{task_id}/cancel")
def cancel_task(task_id: str):
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    workflow_engine.stop_all()
    task_manager.update_task_status(task_id, TaskStatus.CANCELLED)
    
    return {"task_id": task_id, "status": "cancelled"}


def _create_and_start_task(
    task_type: TaskType,
    devices: list,
    ai_type: str,
    runner: Callable[[list, str], dict],
) -> TaskResponse:
    busy_devices = [dev for dev in devices if workflow_engine.is_device_busy(dev)]
    if busy_devices:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "device_busy",
                "message": "One or more devices are already running tasks",
                "busy_devices": busy_devices,
            },
        )

    task = task_manager.create_task(task_type, devices, ai_type, handler=runner)
    if not task_manager.run_task_async(task.task_id):
        raise HTTPException(
            status_code=503,
            detail={
                "code": "queue_full",
                "message": "Task queue is full",
                "task_id": task.task_id,
            },
        )

    return TaskResponse(
        task_id=task.task_id,
        task_type=task.task_type,
        devices=task.devices,
        ai_type=task.ai_type,
        status=task.status,
        created_at=task.created_at,
    )
