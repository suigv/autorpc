"""
设备管理模块
"""
import threading
from common.bot_agent import BotAgent
from .port_calc import calculate_ports
from .config_loader import get_host_ip, get_total_devices, get_default_ai

def parse_device_range(input_str):
    if not input_str:
        return list(range(1, get_total_devices() + 1))
    
    devices = set()
    input_str = input_str.replace(" ", "").lower()
    
    for part in input_str.split(","):
        if "-" in part:
            parts = part.split("-")
            if len(parts) == 2:
                start, end = int(parts[0]), int(parts[1])
                devices.update(range(start, end + 1))
        else:
            try:
                devices.add(int(part))
            except:
                pass
    
    return sorted(list(devices))

def parse_ai_type(input_str):
    if not input_str:
        return get_default_ai()
    
    input_str = input_str.lower().strip()
    if input_str in ["part_time", "part", "兼职", "jp", "paypay"]:
        return "part_time"
    return "volc"

def check_stop_condition(stop_hour):
    import datetime
    return datetime.datetime.now().hour >= stop_hour

class DeviceManager:
    def __init__(self):
        self.host_ip = get_host_ip()
        self.total_devices = get_total_devices()
        
    def is_device_online(self, device_index):
        bot = BotAgent(device_index, self.host_ip)
        return bot.connect()
