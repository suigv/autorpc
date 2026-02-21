from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import logging
import os

from app.api import devices, tasks, config
from app.api.data import router as data_router
from app.api.command import router as command_router
from app.api.stop import router as stop_router
from app.api.websocket import router as websocket_router
from app.core.task_manager import TaskManager

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
app.include_router(stop_router, prefix="/api/tasks", tags=["stop"])
app.include_router(websocket_router)

@app.get("/")
def root():
    return {"message": "MYT RPA API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok", "task": TaskManager().get_runtime_stats()}

# 提供前端页面
web_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")

@app.get("/web")
async def web():
    return FileResponse(os.path.join(web_dir, "index.html"))
