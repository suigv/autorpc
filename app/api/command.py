# app/api/command.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.core.task_log_store import append_task_log, bind_device_task, unbind_device_task
from app.core.device_manager import parse_ai_type
from app.core.config_loader import get_total_devices
from app.core.task_manager import TaskManager
from app.core.workflow_engine import WorkflowEngine
from app.models.task import TaskType

router = APIRouter()
workflow_engine = WorkflowEngine()
task_manager = TaskManager()

class CommandRequest(BaseModel):
    command: str
    device: Optional[int] = None

def parse_command(command: str):
    """解析命令 - 支持自然语言"""
    original_command = command.strip()
    command_lower = original_command.lower()
    
    devices = []
    ai_type = "volc"
    
    import re
    device_patterns = [
        r'(\d+)号机?',
        r'设备(\d+)',
        r'device(\d+)',
        r'#(\d+)',
    ]
    total_devices = get_total_devices()

    for pattern in device_patterns:
        match = re.search(pattern, original_command)
        if match:
            device_num = int(match.group(1))
            if 1 <= device_num <= total_devices:
                devices = [device_num]
                break
    
    if not devices:
        all_numbers = re.findall(r'\d+', original_command)
        device_numbers = [int(n) for n in all_numbers if 1 <= int(n) <= total_devices]
        if device_numbers:
            devices = [device_numbers[-1]]
    
    if '兼职' in original_command or 'part' in command_lower:
        ai_type = "part_time"
    elif '交友' in original_command or 'volc' in command_lower:
        ai_type = "volc"
    
    task_type = None
    full_keywords = ['全套', '完整流程', '完整', 'full flow', 'fullflow']
    if any(kw in original_command for kw in full_keywords):
        task_type = 'full_flow'
    elif any(kw in original_command for kw in ['养号', '养号任务', 'nurture', '互动']):
        task_type = 'nurture_flow'
    elif any(kw in original_command for kw in ['重置', '新机', 'reset', '一键新机']):
        task_type = 'reset_login'
    elif any(kw in original_command for kw in ['登录', 'login', '登陆']):
        task_type = 'login'
    elif any(kw in original_command for kw in ['仿冒', '克隆', 'clone', '资料']):
        task_type = 'clone'
    elif any(kw in original_command for kw in ['关注', 'follow', '截流']):
        task_type = 'follow'
    elif any(kw in original_command for kw in ['私信', 'dm', '回复', 'message']):
        task_type = 'dm'
    elif any(kw in original_command for kw in ['循环', 'loop', '持续']):
        task_type = 'loop'
    
    return task_type, devices, ai_type


def _run_single_task(task_type: str, devices: list, ai_type: str, task_id: str) -> bool:
    """执行单任务类型（非流程任务）"""
    from app.core.workflow_engine import get_stop_event, clear_stop_event

    device_index = devices[0]
    slot_lock = workflow_engine.enter_device_slot(device_index)
    if slot_lock is None:
        append_task_log(
            "设备已有任务在运行，拒绝单任务请求",
            device_index=device_index,
            level="warning",
            task_id=task_id,
            source="command",
        )
        return False

    device_info = workflow_engine.get_device_info(device_index, ai_type)
    stop_event = get_stop_event(devices[0])
    clear_stop_event(device_index)
    bind_device_task(device_index, task_id)
    append_task_log(
        f"任务开始: {task_type}, AI: {ai_type}",
        device_index=device_index,
        task_id=task_id,
        source="command",
    )

    result = True
    try:
        if task_type == 'login':
            from tasks.task_login import run_login_task
            result = run_login_task(device_info, None, stop_event)
        elif task_type == 'dm':
            from tasks.task_reply_dm import run_reply_dm_task
            result = run_reply_dm_task(device_info, None, stop_event)
        elif task_type == 'follow':
            from tasks.task_follow_followers import run_follow_followers_task
            result = run_follow_followers_task(device_info, None, stop_event)
        elif task_type == 'clone':
            from tasks.task_clone_profile import run_clone_profile_task
            result = run_clone_profile_task(device_info, None, stop_event)
        else:
            raise ValueError(f"unsupported single task type: {task_type}")

        return result is not False
    finally:
        append_task_log(
            f"任务线程结束: {task_type}",
            device_index=device_index,
            task_id=task_id,
            source="command",
        )
        unbind_device_task(device_index, task_id)
        clear_stop_event(device_index)
        workflow_engine.leave_device_slot(slot_lock)


def _create_and_start_flow_task(task_type: str, devices: list, ai_type: str, command: str):
    flow_task_map = {
        "full_flow": (TaskType.FULL_FLOW, workflow_engine.run_full_flow),
        "nurture_flow": (TaskType.NURTURE_FLOW, workflow_engine.run_nurture_flow),
        "reset_login": (TaskType.RESET_LOGIN, workflow_engine.run_reset_login),
        "loop": (TaskType.NURTURE_FLOW, workflow_engine.run_nurture_flow),
    }

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

    task_enum, handler = flow_task_map[task_type]
    task = task_manager.create_task(task_enum, devices, ai_type, handler=handler)
    if not task_manager.run_task_async(task.task_id):
        append_task_log(
            "任务队列已满，拒绝执行",
            device_index=devices[0],
            level="error",
            task_id=task.task_id,
            source="command",
        )
        raise HTTPException(
            status_code=503,
            detail={
                "code": "queue_full",
                "message": "Task queue is full",
                "task_id": task.task_id,
            },
        )

    append_task_log(
        f"接收命令: {command} -> {task_type}",
        device_index=devices[0],
        task_id=task.task_id,
        source="command",
    )

    return {
        "status": "ok",
        "task_id": task.task_id,
        "task_type": task_type,
        "devices": devices,
        "message": f"任务已启动: {task_type}, 设备: {devices}, AI: {ai_type}",
    }


def _create_and_start_single_task(task_type: str, devices: list, ai_type: str, command: str):
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

    def _single_task_handler(handler_devices: list, handler_ai_type: str):
        try:
            ok = _run_single_task(task_type, handler_devices, handler_ai_type, task.task_id)
            if not ok:
                raise RuntimeError("single task returned false")
            return {"task_type": task_type, "ok": True}
        except Exception as exc:
            append_task_log(
                f"任务异常: {exc}",
                device_index=handler_devices[0],
                level="error",
                task_id=task.task_id,
                source="command",
            )
            raise

    task = task_manager.create_task(
        TaskType.SINGLE_TASK,
        devices,
        ai_type,
        handler=_single_task_handler,
    )

    append_task_log(
        f"接收命令: {command} -> {task_type}",
        device_index=devices[0],
        task_id=task.task_id,
        source="command",
    )

    if not task_manager.run_task_async(task.task_id):
        append_task_log(
            "任务队列已满，拒绝执行",
            device_index=devices[0],
            level="error",
            task_id=task.task_id,
            source="command",
        )
        raise HTTPException(
            status_code=503,
            detail={
                "code": "queue_full",
                "message": "Task queue is full",
                "task_id": task.task_id,
            },
        )

    return {
        "status": "ok",
        "task_id": task.task_id,
        "task_type": task_type,
        "devices": devices,
        "message": f"任务已启动: {task_type}, 设备: {devices}, AI: {ai_type}",
    }


@router.post("/execute")
def execute_command(req: CommandRequest):
    """执行命令"""
    task_type, devices, ai_type = parse_command(req.command)
    
    if not task_type:
        append_task_log("命令解析失败", level="error", source="command")
        raise HTTPException(
            status_code=400,
            detail={
                "code": "invalid_command",
                "message": "Unable to parse command",
            },
        )
    
    if not devices:
        devices = [req.device] if req.device else [1]

    ai_type = parse_ai_type(ai_type)

    command = req.command.strip()
    if task_type in {"full_flow", "nurture_flow", "reset_login", "loop"}:
        return _create_and_start_flow_task(task_type, devices, ai_type, command)

    return _create_and_start_single_task(task_type, devices, ai_type, command)
