"""
任务插件基类
"""
import time
import logging
from abc import ABC, abstractmethod
from typing import Optional
from threading import Event

logger = logging.getLogger(__name__)


class BaseTask(ABC):
    name: str = "base_task"
    
    def __init__(self, device_info: dict, stop_event: Optional[Event] = None):
        self.device_info = device_info
        self.stop_event = stop_event or Event()
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
    
    @abstractmethod
    def execute(self) -> bool:
        """执行任务，返回 True 表示成功"""
        pass
    
    def should_stop(self) -> bool:
        return self.stop_event.is_set()
    
    def sleep(self, seconds: float):
        time.sleep(seconds)
