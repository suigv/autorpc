"""
端口计算模块
"""

def calculate_ports(device_index):
    base_port = 30000 + (device_index - 1) * 100
    rpa_port = base_port + 2
    api_port = base_port + 1
    return rpa_port, api_port

def get_device_info(device_index, host_ip):
    rpa_port, api_port = calculate_ports(device_index)
    return {
        "index": device_index,
        "ip": host_ip,
        "rpa_port": rpa_port,
        "api_port": api_port
    }
