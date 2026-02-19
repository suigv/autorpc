"""
任务 API
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from app.models.task import TaskRequest, TaskResponse, TaskDetailResponse, TaskType, TaskStatus
from app.core.workflow_engine import WorkflowEngine
from app.core.device_manager import parse_device_range, parse_ai_type
from app.core.task_manager import TaskManager
from app.core.task_log_store import get_task_logs
from common.runtime_state import reset_runtime_state

router = APIRouter()
workflow_engine = WorkflowEngine()
task_manager = TaskManager()


@router.post("/full-flow", response_model=TaskResponse)
def create_full_flow_task(request: TaskRequest):
    devices = request.devices
    ai_type = parse_ai_type(request.ai_type)
    
    task = task_manager.create_task(TaskType.FULL_FLOW, devices, ai_type)
    
    def handler(devices, ai_type):
        return workflow_engine.run_full_flow(devices, ai_type)
    
    task_manager.register_handler(TaskType.FULL_FLOW, handler)
    task_manager.run_task_async(task.task_id)
    
    return TaskResponse(
        task_id=task.task_id,
        task_type=task.task_type,
        devices=task.devices,
        ai_type=task.ai_type,
        status=task.status,
        created_at=task.created_at
    )


@router.post("/nurture-flow", response_model=TaskResponse)
def create_nurture_flow_task(request: TaskRequest):
    devices = request.devices
    ai_type = parse_ai_type(request.ai_type)
    
    task = task_manager.create_task(TaskType.NURTURE_FLOW, devices, ai_type)
    
    def handler(devices, ai_type):
        return workflow_engine.run_nurture_flow(devices, ai_type)
    
    task_manager.register_handler(TaskType.NURTURE_FLOW, handler)
    task_manager.run_task_async(task.task_id)
    
    return TaskResponse(
        task_id=task.task_id,
        task_type=task.task_type,
        devices=task.devices,
        ai_type=task.ai_type,
        status=task.status,
        created_at=task.created_at
    )


@router.post("/reset-login", response_model=TaskResponse)
def create_reset_login_task(request: TaskRequest):
    devices = request.devices
    ai_type = parse_ai_type(request.ai_type)
    
    task = task_manager.create_task(TaskType.RESET_LOGIN, devices, ai_type)
    
    def handler(devices, ai_type):
        return workflow_engine.run_reset_login(devices, ai_type)
    
    task_manager.register_handler(TaskType.RESET_LOGIN, handler)
    task_manager.run_task_async(task.task_id)
    
    return TaskResponse(
        task_id=task.task_id,
        task_type=task.task_type,
        devices=task.devices,
        ai_type=task.ai_type,
        status=task.status,
        created_at=task.created_at
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
