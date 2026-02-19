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
    original_command = command.strip()
    command = original_command.lower()
    
    # 解析设备号
    devices = []
    ai_type = "volc"
    
    parts = original_command.split()
    if not parts:
        return None, None, None
    
    # 提取设备号 - 使用原始命令
    import re
    # 查找命令中的所有数字，选择最后一个作为设备号
    all_numbers = re.findall(r'\d+', original_command)
    device_numbers = [n for n in all_numbers if int(n) <= 10]
    if device_numbers:
        last_num = int(device_numbers[-1])
        if last_num >= 1 and last_num <= 10:
            devices = [last_num]
    
    # 提取 AI 类型 - 使用原始命令
    if 'part' in original_command.lower() or '兼职' in original_command:
        ai_type = "part_time"
    elif 'volc' in original_command.lower() or '交友' in original_command:
        ai_type = "volc"
    
    # 解析任务类型 - 使用原始命令
    task_type = None
    if '全套' in original_command or 'full' in original_command.lower():
        task_type = 'full_flow'
    elif '养号' in original_command or 'nurture' in original_command.lower():
        task_type = 'nurture_flow'
    elif '重置' in original_command or 'reset' in original_command.lower():
        task_type = 'reset_login'
    elif '登录' in original_command or 'login' in original_command.lower():
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
