"""
端口计算模块
"""

BASE_PORT = 30000
PORT_STEP = 100


def calculate_ports(device_index: int) -> tuple[int, int]:
    base_port = BASE_PORT + (device_index - 1) * PORT_STEP
    rpa_port = base_port + 2
    api_port = base_port + 1
    return rpa_port, api_port


def get_device_info(device_index: int, host_ip: str) -> dict:
    rpa_port, api_port = calculate_ports(device_index)
    return {
        "index": device_index,
        "ip": host_ip,
        "rpa_port": rpa_port,
        "api_port": api_port
    }
