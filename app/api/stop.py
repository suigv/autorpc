# app/api/stop.py
from fastapi import APIRouter
import threading

from app.core.task_log_store import append_task_log

router = APIRouter()

def _force_stop_app_in_background(device_index: int):
    """后台强制关闭设备上的 X App，避免阻塞 API 响应"""
    from common.bot_agent import BotAgent
    from app.core.config_loader import get_host_ip

    bot = None
    try:
        bot = BotAgent(device_index, get_host_ip())
        if bot.connect():
            bot.force_stop_app()
    except Exception:
        pass
    finally:
        try:
            if bot:
                bot.quit()
        except Exception:
            pass

@router.post("/stop")
def stop_task():
    """停止所有运行中的任务"""
    from app.core.workflow_engine import WorkflowEngine
    
    engine = WorkflowEngine()
    
    # 触发所有设备的停止事件
    for device_index in range(1, 11):
        engine.stop_device(device_index)
        append_task_log("收到全局停止请求", device_index=device_index, level="warning", source="stop")
        t = threading.Thread(target=_force_stop_app_in_background, args=(device_index,), daemon=True)
        t.start()
    
    return {"status": "ok", "message": "停止信号已发送"}

@router.post("/stop/{device_index}")
def stop_single_device(device_index: int):
    """停止指定设备的任务"""
    from app.core.workflow_engine import WorkflowEngine
    
    engine = WorkflowEngine()
    result = engine.stop_device(device_index)
    append_task_log("收到设备停止请求", device_index=device_index, level="warning", source="stop")
    
    if result:
        t = threading.Thread(target=_force_stop_app_in_background, args=(device_index,), daemon=True)
        t.start()
    
    return {"status": "ok", "message": f"设备{device_index}停止信号已发送"}
