"""
配置 API
"""
from fastapi import APIRouter, HTTPException

from app.models.config import Config, ConfigUpdate
from app.core.config_loader import (
    get_host_ip, get_total_devices, get_default_ai,
    get_stop_hour, get_cycle_interval, update_host_ip, ConfigLoader
)

router = APIRouter()


@router.get("/", response_model=Config)
def get_config():
    return Config(
        host_ip=get_host_ip(),
        total_devices=get_total_devices(),
        default_ai=get_default_ai(),
        stop_hour=get_stop_hour(),
        cycle_interval=get_cycle_interval()
    )


@router.put("/", response_model=Config)
def update_config(config: ConfigUpdate):
    update_data = config.model_dump(exclude_none=True)
    if update_data:
        ConfigLoader.update(**update_data)
    return get_config()


@router.get("/host-ip")
def get_host_ip_endpoint():
    return {"host_ip": get_host_ip()}


@router.put("/host-ip")
def update_host_ip_endpoint(host_ip: str):
    update_host_ip(host_ip)
    return {"host_ip": host_ip, "status": "updated"}
