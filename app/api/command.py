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
    """解析命令 - 支持自然语言"""
    original_command = command.strip()
    command_lower = original_command.lower()
    
    # 解析设备号
    devices = []
    ai_type = "volc"
    
    # 提取设备号 - 多种模式
    import re
    # 模式1: "3号", "3号机", "设备3", "设备3号"
    device_patterns = [
        r'(\d+)号机?',      # 3号, 3号机
        r'设备(\d+)',       # 设备3
        r'device(\d+)',     # device3
        r'#(\d+)',         # #3
    ]
    for pattern in device_patterns:
        match = re.search(pattern, original_command)
        if match:
            device_num = int(match.group(1))
            if 1 <= device_num <= 10:
                devices = [device_num]
                break
    
    # 如果没找到，使用末尾数字
    if not devices:
        all_numbers = re.findall(r'\d+', original_command)
        device_numbers = [int(n) for n in all_numbers if 1 <= int(n) <= 10]
        if device_numbers:
            devices = [device_numbers[-1]]
    
    # 提取 AI 类型
    if '兼职' in original_command or 'part' in command_lower:
        ai_type = "part_time"
    elif '交友' in original_command or 'volc' in command_lower:
        ai_type = "volc"
    
    # 解析任务类型 - 多种说法
    task_type = None
    
    # 全套/完整流程
    full_keywords = ['全套', '完整流程', '完整', 'full flow', 'fullflow']
    if any(kw in original_command for kw in full_keywords):
        task_type = 'full_flow'
    
    # 养号
    elif any(kw in original_command for kw in ['养号', '养号任务', 'nurture', '互动']):
        task_type = 'nurture_flow'
    
    # 重置/新机
    elif any(kw in original_command for kw in ['重置', '新机', 'reset', '一键新机']):
        task_type = 'reset_login'
    
    # 登录
    elif any(kw in original_command for kw in ['登录', 'login', '登陆']):
        task_type = 'login'
    
    # 仿冒/克隆
    elif any(kw in original_command for kw in ['仿冒', '克隆', 'clone', '资料']):
        task_type = 'clone'
    
    # 关注
    elif any(kw in original_command for kw in ['关注', 'follow', '截流']):
        task_type = 'follow'
    
    # 私信
    elif any(kw in original_command for kw in ['私信', 'dm', '回复', 'message']):
        task_type = 'dm'
    
    return task_type, devices, ai_type

@router.post("/execute")
def execute_command(req: CommandRequest):
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
    from app.core.config_loader import get_host_ip
    
    # 调试：打印配置
    print(f"DEBUG: Host IP = {get_host_ip()}")
    
    engine = WorkflowEngine()
    print(f"DEBUG: Engine host_ip = {engine.host_ip}")
    
    # 调试BotAgent
    from common.bot_agent import BotAgent
    bot = BotAgent(3, engine.host_ip)
    print(f"DEBUG: BotAgent rpa lib path = {bot.rpa._lib_PATH}")
    bot_result = bot.connect()
    print(f"DEBUG: BotAgent connect result = {bot_result}")
    if bot_result:
        bot.quit()
    
    # 直接执行任务（不使用background_tasks，确保日志输出）
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
        return {"status": "error", "message": str(e)}
    
    return {
        "status": "ok", 
        "message": f"任务完成: {task_type}, 设备: {devices}, AI: {ai_type}"
    }
