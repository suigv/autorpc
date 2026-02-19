# app/api/command.py
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import threading

router = APIRouter()

class CommandRequest(BaseModel):
    command: str
    device: int = None

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
    
    return task_type, devices, ai_type


def run_task_in_thread(task_type, devices, ai_type):
    """在线程中执行任务"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from app.core.workflow_engine import WorkflowEngine
    
    engine = WorkflowEngine()
    
    try:
        if task_type == 'full_flow':
            engine.run_full_flow(devices, ai_type)
        elif task_type == 'nurture_flow':
            engine.run_nurture_flow(devices, ai_type)
        elif task_type == 'reset_login':
            engine.run_reset_login(devices, ai_type)
    except Exception as e:
        print(f"任务执行异常: {e}")


@router.post("/execute")
def execute_command(req: CommandRequest, background_tasks: BackgroundTasks):
    """执行命令"""
    task_type, devices, ai_type = parse_command(req.command)
    
    if not task_type:
        return {"status": "error", "message": "无法解析命令"}
    
    if not devices:
        devices = [req.device] if req.device else [1]
    
    # 启动后台线程执行任务
    thread = threading.Thread(target=run_task_in_thread, args=(task_type, devices, ai_type))
    thread.daemon = True
    thread.start()
    
    return {
        "status": "ok", 
        "message": f"任务已启动: {task_type}, 设备: {devices}, AI: {ai_type}"
    }
