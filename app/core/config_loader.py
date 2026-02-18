"""
配置加载模块
"""
import json
from pathlib import Path
from typing import Optional

CONFIG_FILE = Path(__file__).parent.parent.parent / "config" / "devices.json"


class ConfigLoader:
    _config: Optional[dict] = None

    @classmethod
    def load(cls) -> dict:
        if cls._config is None:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cls._config = json.load(f)
        return cls._config

    @classmethod
    def reload(cls) -> dict:
        cls._config = None
        return cls.load()

    @classmethod
    def get(cls, key: str, default=None):
        return cls.load().get(key, default)

    @classmethod
    def update(cls, **kwargs):
        config = cls.load()
        config.update(kwargs)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        cls._config = config


def get_host_ip() -> str:
    return ConfigLoader.get("host_ip")


def get_total_devices() -> int:
    return ConfigLoader.get("total_devices", 10)


def get_default_ai() -> str:
    return ConfigLoader.get("default_ai", "volc")


def get_stop_hour() -> int:
    return ConfigLoader.get("stop_hour", 18)


def get_cycle_interval() -> int:
    return ConfigLoader.get("cycle_interval", 15)


def update_host_ip(new_ip: str):
    ConfigLoader.update(host_ip=new_ip)
