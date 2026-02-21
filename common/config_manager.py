# common/config_manager.py
import os

from app.core.config_loader import ConfigLoader, get_default_ai
from common.ToolsKit import ToolsKit


class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.tools = ToolsKit()
        self.root_path = self.tools.GetRootPath()
        self.log_dir = os.path.join(self.root_path, "log")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # 兼容旧代码中未落盘的运行时键
        self.runtime_config = {
            "delay": 5,
            "schedule_enabled": False,
        }

    def get_file_path(self, filename, ai_type=None):
        """统一获取文件路径，支持根据 ai_type 加前缀"""
        if ai_type:
            prefix = "jy" if ai_type == "volc" else "jz"
            filename = f"{prefix}_{filename}"
            return os.path.join(self.log_dir, filename)
        return os.path.join(self.root_path, filename)

    def get_backup_file(self, ai_type):
        """获取备用博主文件路径"""
        filename = "交友博主.txt" if ai_type == "volc" else "兼职博主.txt"
        return os.path.join(self.root_path, filename)

    def update_runtime(self, key, value):
        if key in ("ip", "host_ip"):
            ConfigLoader.update(host_ip=value)
            return
        if key in ("ai_type", "default_ai"):
            ConfigLoader.update(default_ai=value)
            return
        self.runtime_config[key] = value

    @property
    def ai_type(self):
        return get_default_ai()

# 全局单例
cfg = ConfigManager()
