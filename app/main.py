from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api import devices, tasks, config

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

@app.get("/")
def root():
    return {"message": "MYT RPA API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok"}
