# common/config_manager.py
import os
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
            
        # 默认运行时配置
        self.runtime_config = {
            "ip": "192.168.1.215",
            "delay": 5,
            "ai_type": "volc", # volc / part_time
            "schedule_enabled": False
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
        self.runtime_config[key] = value

    @property
    def ai_type(self):
        return self.runtime_config.get("ai_type", "volc")

# 全局单例
cfg = ConfigManager()