# app/api/command.py
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import threading

router = APIRouter()

# 存储运行中的任务
running_tasks = {}

class CommandRequest(BaseModel):
    command: str
    device: int = None

def parse_command(command: str):
    """解析命令"""
    command = command.strip().lower()
    
    # 解析设备号
    devices = []
    ai_type = "volc"
    
    parts = command.split()
    if not parts:
        return None, None, None
    
    # 提取设备号
    import re
    device_match = re.search(r'(\d+(?:-\d+)?)', parts[-1] if len(parts) > 1 else parts[0])
    if device_match:
        device_str = device_match.group(1)
        if '-' in device_str:
            start, end = map(int, device_str.split('-'))
            devices = list(range(start, end + 1))
        else:
            devices = [int(device_str)]
    
    # 提取 AI 类型
    if 'part' in command or '兼职' in command:
        ai_type = "part_time"
    elif 'volc' in command or '交友' in command:
        ai_type = "volc"
    
    # 解析任务类型
    task_type = None
    if '全套' in command or 'full' in command:
        task_type = 'full_flow'
    elif '养号' in command or 'nurture' in command:
        task_type = 'nurture_flow'
    elif '重置' in command or 'reset' in command:
        task_type = 'reset_login'
    elif '登录' in command or 'login' in command:
        task_type = 'login'
    
    return task_type, devices, ai_type

@router.post("/execute")
async def execute_command(req: CommandRequest, background_tasks: BackgroundTasks):
    """执行命令"""
    task_type, devices, ai_type = parse_command(req.command)
    
    if not task_type:
        return {"status": "error", "message": "无法解析命令"}
    
    if not devices:
        devices = [req.device] if req.device else [1]
    
    # 导入工作流引擎
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from app.core.workflow_engine import WorkflowEngine
    
    engine = WorkflowEngine()
    
    def run_task():
        if task_type == 'full_flow':
            engine.run_full_flow(devices, ai_type)
        elif task_type == 'nurture_flow':
            engine.run_nurture_flow(devices, ai_type)
        elif task_type == 'reset_login':
            engine.run_reset_login(devices, ai_type)
    
    background_tasks.add_task(run_task)
    
    return {
        "status": "ok", 
        "message": f"任务已启动: {task_type}, 设备: {devices}, AI: {ai_type}"
    }
