from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import WebSocket, WebSocketDisconnect
import logging
import os

from app.api import devices, tasks, config
from app.api.data import router as data_router
from app.api.command import router as command_router
from app.core.log_manager import log_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="MYT RPA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(devices.router, prefix="/api/devices", tags=["devices"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(config.router, prefix="/api/config", tags=["config"])
app.include_router(data_router, prefix="/api/data", tags=["data"])
app.include_router(command_router, prefix="/api/tasks", tags=["command"])

@app.get("/")
def root():
    return {"message": "MYT RPA API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok"}

# 提供前端页面
web_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")

@app.get("/web")
async def web():
    return FileResponse(os.path.join(web_dir, "index.html"))

# WebSocket日志端点
@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    """WebSocket日志实时推送"""
    from common.logger import log_manager as logger
    from app.core.log_manager import log_manager as ws_manager
    
    await websocket.accept()
    ws_manager.disconnect(websocket)
    ws_manager._clients.append(websocket)
    
    # 设置广播函数到logger
    async def broadcast(msg):
        try:
            await websocket.send_text(msg)
        except:
            pass
    
    logger.set_ws_broadcast(broadcast)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                import json
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
            except:
                pass
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
