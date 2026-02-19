from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import logging
import os

from app.api import devices, tasks, config
from app.api.websocket import router as ws_router
from app.api.data import router as data_router
from app.api.command import router as command_router

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
app.include_router(ws_router, tags=["websocket"])
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
