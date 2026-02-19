# app/api/stop.py
from fastapi import APIRouter
import threading

router = APIRouter()

# 全局停止事件
stop_events = {}

@router.post("/stop")
async def stop_task():
    """停止所有运行中的任务"""
    from app.core.workflow_engine import WorkflowEngine
    
    engine = WorkflowEngine()
    
    # 触发所有设备的停止事件
    for device_index in range(1, 11):
        engine.stop_device(device_index)
    
    return {"status": "ok", "message": "停止信号已发送"}

@router.post("/stop/{device_index}")
async def stop_single_device(device_index: int):
    """停止指定设备的任务"""
    from app.core.workflow_engine import WorkflowEngine
    
    engine = WorkflowEngine()
    result = engine.stop_device(device_index)
    
    if result:
        # 额外：强制停止设备上的X App
        from common.bot_agent import BotAgent
        from app.core.config_loader import get_host_ip
        try:
            bot = BotAgent(device_index, get_host_ip())
            bot.connect()
            bot.force_stop_app()
            bot.quit()
        except:
            pass
    
    return {"status": "ok", "message": f"设备{device_index}停止信号已发送"}
