# common/base_task.py
from abc import ABC, abstractmethod
from common.bot_agent import BotAgent
from common.logger import log_manager

class BaseTask(ABC):
    def __init__(self, device_info, stop_event):
        self.device_info = device_info
        self.index = device_info['index']
        self.ip = device_info['ip']
        self.stop_event = stop_event
        self.bot = BotAgent(self.index, self.ip)
        self.ai_type = device_info.get('ai_type', 'volc')

    def log(self, msg, level="info"):
        log_manager.log(self.index, msg, level)

    def connect(self):
        if not self.bot.connect():
            self.log("❌ 连接失败", "error")
            return False
        return True

    @abstractmethod
    def run(self):
        """子类必须实现此方法"""
        pass

    def execute(self):
        """统一执行入口，包含异常处理"""
        try:
            if self.stop_event.is_set(): return
            if not self.connect(): return
            
            self.run()
            
        except Exception as e:
            self.log(f"❌ 任务异常: {e}", "error")
            import traceback
            traceback.print_exc()
        finally:
            self.bot.quit()
