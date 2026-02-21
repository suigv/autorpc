# app/api/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from common.logger import log_manager as runtime_logger

router = APIRouter()
_clients = []
_logger_bridge_ready = False


async def _broadcast(message: str):
    disconnected = []
    for client in list(_clients):
        try:
            await client.send_text(message)
        except Exception:
            disconnected.append(client)

    for client in disconnected:
        if client in _clients:
            _clients.remove(client)


def _ensure_logger_bridge():
    global _logger_bridge_ready
    if _logger_bridge_ready:
        return
    runtime_logger.set_ws_broadcast(_broadcast)
    _logger_bridge_ready = True

@router.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    """WebSocket日志实时推送"""
    _ensure_logger_bridge()
    await websocket.accept()
    if websocket not in _clients:
        _clients.append(websocket)

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
        pass
    finally:
        if websocket in _clients:
            _clients.remove(websocket)
