from pydantic import BaseModel
from typing import Optional


class Config(BaseModel):
    host_ip: str
    total_devices: int
    default_ai: str
    stop_hour: int
    cycle_interval: int


class ConfigUpdate(BaseModel):
    host_ip: Optional[str] = None
    total_devices: Optional[int] = None
    default_ai: Optional[str] = None
    stop_hour: Optional[int] = None
    cycle_interval: Optional[int] = None
