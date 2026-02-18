"""
设备管理器
"""
import threading
import logging
from typing import Dict, Optional
from datetime import datetime

from app.core.config_loader import get_host_ip, get_stop_hour
from app.core.port_calc import calculate_ports
from app.models.device import DeviceStatus, AIType

logger = logging.getLogger(__name__)


class Device:
    def __init__(self, index: int, ai_type: AIType = AIType.VOLC):
        self.index = index
        self.ai_type = ai_type
        self.status = DeviceStatus.IDLE
        self.current_task: Optional[str] = None
        self.message: Optional[str] = None
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "ai_type": self.ai_type.value,
            "status": self.status.value,
            "current_task": self.current_task,
            "message": self.message,
            "updated_at": self.updated_at.isoformat()
        }


class DeviceManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._devices: Dict[int, Device] = {}
            self._host_ip = get_host_ip()
            self._initialized = True

    def get_device(self, index: int, ai_type: AIType = AIType.VOLC) -> Device:
        if index not in self._devices:
            self._devices[index] = Device(index, ai_type)
        return self._devices[index]

    def get_all_devices(self) -> Dict[int, Device]:
        return self._devices

    def get_device_info(self, index: int) -> dict:
        device = self.get_device(index)
        rpa_port, api_port = calculate_ports(index)
        return {
            "index": index,
            "ip": self._host_ip,
            "rpa_port": rpa_port,
            "api_port": api_port,
            "ai_type": device.ai_type.value,
            "status": device.status.value if hasattr(device.status, 'value') else device.status,
            "current_task": device.current_task,
            "message": device.message
        }

    def set_device_status(self, index: int, status: DeviceStatus, task: str = None, message: str = None):
        device = self.get_device(index)
        device.status = status
        if task:
            device.current_task = task
        if message:
            device.message = message
        device.updated_at = datetime.now()

    def start_device_task(self, index: int, task_func, *args, **kwargs):
        device = self.get_device(index)
        if device.thread and device.thread.is_alive():
            logger.warning(f"Device {index} is already running a task")
            return False

        device.stop_event.clear()
        device.thread = threading.Thread(target=task_func, args=args, kwargs=kwargs)
        device.thread.start()
        return True

    def stop_device_task(self, index: int):
        device = self.get_device(index)
        if device.thread and device.thread.is_alive():
            device.stop_event.set()
            return True
        return False


def parse_device_range(device_str: str) -> list[int]:
    devices = set()
    for part in device_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            devices.update(range(int(start), int(end) + 1))
        else:
            devices.add(int(part))
    return sorted(devices)


def parse_ai_type(ai_type: str) -> str:
    ai_type = ai_type.lower().strip()
    if ai_type in ["volc", "volcano", "火山"]:
        return "volc"
    elif ai_type in ["part_time", "兼职", "parttime"]:
        return "part_time"
    return "volc"


def check_stop_condition(stop_hour: int = None) -> bool:
    if stop_hour is None:
        stop_hour = get_stop_hour()
    from datetime import datetime
    return datetime.now().hour >= stop_hour
