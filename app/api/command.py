# app/api/command.py
from fastapi import APIRouter
from pydantic import BaseModel
import threading
from typing import Optional
import uuid

from app.core.task_log_store import append_task_log, bind_device_task, unbind_device_task

router = APIRouter()

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
    for pattern in device_patterns:
        match = re.search(pattern, original_command)
        if match:
            device_num = int(match.group(1))
            if 1 <= device_num <= 10:
                devices = [device_num]
                break
    
    if not devices:
        all_numbers = re.findall(r'\d+', original_command)
        device_numbers = [int(n) for n in all_numbers if 1 <= int(n) <= 10]
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


def run_task_in_thread(task_type, devices, ai_type, task_id):
    """在线程中执行任务"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from app.core.workflow_engine import WorkflowEngine, get_stop_event, clear_stop_event
    from app.core.config_loader import get_host_ip
    from app.core.port_calc import calculate_ports
    
    engine = WorkflowEngine()
    
    rpa_port, api_port = calculate_ports(devices[0])
    device_info = {
        "ip": get_host_ip(),
        "index": devices[0],
        "rpa_port": rpa_port,
        "api_port": api_port,
        "ai_type": ai_type
    }
    
    stop_event = get_stop_event(devices[0])
    clear_stop_event(devices[0])
    bind_device_task(devices[0], task_id)
    append_task_log(
        f"任务开始: {task_type}, AI: {ai_type}",
        device_index=devices[0],
        task_id=task_id,
        source="command",
    )
    
    try:
        if task_type == 'full_flow':
            engine.run_full_flow(devices, ai_type)
        elif task_type == 'nurture_flow':
            engine.run_nurture_flow(devices, ai_type)
        elif task_type == 'reset_login':
            engine.run_reset_login(devices, ai_type)
        elif task_type == 'login':
            from tasks.task_login import run_login_task
            run_login_task(device_info, None, stop_event)
        elif task_type == 'dm':
            from tasks.task_reply_dm import run_reply_dm_task
            run_reply_dm_task(device_info, None, stop_event)
        elif task_type == 'follow':
            from tasks.task_follow_followers import run_follow_followers_task
            run_follow_followers_task(device_info, None, stop_event)
        elif task_type == 'clone':
            from tasks.task_clone_profile import run_clone_profile_task
            run_clone_profile_task(device_info, None, stop_event)
        elif task_type == 'loop':
            # 循环任务 = 养号流程（无限循环直到停止）
            engine.run_nurture_flow(devices, ai_type)
    except Exception as e:
        print(f"任务执行异常: {e}")
        append_task_log(
            f"任务异常: {e}",
            device_index=devices[0],
            level="error",
            task_id=task_id,
            source="command",
        )
    finally:
        append_task_log(
            f"任务线程结束: {task_type}",
            device_index=devices[0],
            task_id=task_id,
            source="command",
        )
        unbind_device_task(devices[0], task_id)
        clear_stop_event(devices[0])


@router.post("/execute")
def execute_command(req: CommandRequest):
    """执行命令"""
    task_type, devices, ai_type = parse_command(req.command)
    
    if not task_type:
        append_task_log("命令解析失败", level="error", source="command")
        return {"status": "error", "message": "无法解析命令"}
    
    if not devices:
        devices = [req.device] if req.device else [1]

    task_id = uuid.uuid4().hex[:12]
    append_task_log(
        f"接收命令: {req.command.strip()} -> {task_type}",
        device_index=devices[0],
        task_id=task_id,
        source="command",
    )
    
    # 启动后台线程执行任务
    thread = threading.Thread(target=run_task_in_thread, args=(task_type, devices, ai_type, task_id))
    thread.daemon = True
    thread.start()
    
    return {
        "status": "ok", 
        "task_id": task_id,
        "task_type": task_type,
        "devices": devices,
        "message": f"任务已启动: {task_type}, 设备: {devices}, AI: {ai_type}"
    }
