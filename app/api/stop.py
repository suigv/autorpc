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
