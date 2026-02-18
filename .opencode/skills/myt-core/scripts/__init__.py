"""
MYT Core Skills Wrapper
让 OpenCode 能调用 demo_py_x64.skills 模块
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from skills.core import (
    WorkflowEngine,
    parse_device_range,
    parse_ai_type,
    get_host_ip,
    get_total_devices,
    get_stop_hour,
    get_cycle_interval,
    update_host_ip
)

__all__ = [
    "WorkflowEngine",
    "parse_device_range", 
    "parse_ai_type",
    "get_host_ip",
    "get_total_devices",
    "get_stop_hour",
    "get_cycle_interval",
    "update_host_ip"
]
