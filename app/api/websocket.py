# app/api/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.log_manager import log_manager
import json
import asyncio

router = APIRouter()

@router.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    """WebSocket日志实时推送"""
    await log_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 可以处理客户端发送的消息
            try:
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
            except:
                pass
    except WebSocketDisconnect:
        log_manager.disconnect(websocket)
