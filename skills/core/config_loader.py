"""
MYT Skills 核心模块
"""
import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent.parent / "config" / "devices.json"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_host_ip():
    return load_config()["host_ip"]

def get_total_devices():
    return load_config()["total_devices"]

def get_default_ai():
    return load_config()["default_ai"]

def get_stop_hour():
    return load_config()["stop_hour"]

def get_cycle_interval():
    return load_config().get("cycle_interval", 15)

def update_host_ip(new_ip):
    config = load_config()
    config["host_ip"] = new_ip
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
