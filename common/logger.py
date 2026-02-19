# common/logger.py
import logging
import sys
import os
import atexit

class GuiLogHandler(logging.Handler):
    """自定义 Handler，将日志发送到 GUI 回调"""
    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback

    def emit(self, record):
        if self.callback:
            msg = self.format(record)
            self.callback(msg)
        # 立即刷新
        self.flush()

class Logger:
    _instance = None
    _gui_callback = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        if Logger._initialized:
            return
        
        self.logger = logging.getLogger("MytLogger")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        
        # 清除已有 handlers
        self.logger.handlers.clear()
        
        # 控制台输出 - 实时刷新
        console = logging.StreamHandler(sys.stdout)
        console.stream = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        
        Logger._initialized = True

    def set_gui_callback(self, callback):
        """设置 GUI 日志回调函数"""
        self._gui_callback = callback
        # 移除旧的 GUI handler (如果有)
        for h in self.logger.handlers:
            if isinstance(h, GuiLogHandler):
                self.logger.removeHandler(h)
        
        # 添加新的
        gui_handler = GuiLogHandler(callback)
        gui_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S'))
        self.logger.addHandler(gui_handler)

    def flush(self):
        """强制刷新所有 handler"""
        for handler in self.logger.handlers:
            handler.flush()

    def log(self, device_index, message, level="info"):
        full_msg = f"[Dev {device_index}] {message}"
        if level == "info":
            self.logger.info(full_msg)
        elif level == "error":
            self.logger.error(full_msg)
        elif level == "warning":
            self.logger.warning(full_msg)
        # 立即刷新输出
        self.flush()

# 全局单例
log_manager = Logger()
logger = log_manager.logger # 兼容旧代码直接引用 logger
