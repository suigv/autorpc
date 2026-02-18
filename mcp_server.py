"""
MYT MCP Server (简化版)
直接调用 API 接口
"""
import json
import subprocess
import sys

API_BASE = "http://localhost:8000"


def call_api(endpoint: str, method: str = "GET", data: dict = None):
    import requests
    url = f"{API_BASE}{endpoint}"
    if method == "GET":
        r = requests.get(url)
    elif method == "POST":
        r = requests.post(url, json=data)
    return r.json()


def handle_request(req: dict):
    method = req.get("method")
    params = req.get("params", {})
    
    try:
        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req.get("id"),
                "result": {
                    "tools": [
                        {
                            "name": "run_full_flow",
                            "description": "执行完整流程 (一键新机->登录->抓博主->克隆->关注->循环养号)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "devices": {"type": "string", "description": "设备范围，如 '1-5' 或 '1,3,5'"},
                                    "ai_type": {"type": "string", "description": "AI类型: volc=交友, part_time=兼职", "default": "volc"}
                                },
                                "required": ["devices"]
                            }
                        },
                        {
                            "name": "run_nurture_flow",
                            "description": "执行养号流程",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "devices": {"type": "string", "description": "设备范围"},
                                    "ai_type": {"type": "string", "default": "volc"}
                                },
                                "required": ["devices"]
                            }
                        },
                        {
                            "name": "run_reset_login",
                            "description": "执行重置登录",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "devices": {"type": "string"},
                                    "ai_type": {"type": "string", "default": "volc"}
                                },
                                "required": ["devices"]
                            }
                        },
                        {
                            "name": "get_config",
                            "description": "获取当前配置",
                            "inputSchema": {"type": "object", "properties": {}}
                        },
                        {
                            "name": "set_host_ip",
                            "description": "设置设备IP",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "ip": {"type": "string"}
                                },
                                "required": ["ip"]
                            }
                        },
                        {
                            "name": "list_devices",
                            "description": "列出所有设备",
                            "inputSchema": {"type": "object", "properties": {}}
                        }
                    ]
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "run_full_flow":
                result = call_api("/api/tasks/full-flow", "POST", {
                    "devices": _parse_devices(arguments.get("devices", "1")),
                    "ai_type": arguments.get("ai_type", "volc")
                })
                return {"jsonrpc": "2.0", "id": req.get("id"), "result": {"content": [{"type": "text", "text": str(result)}]}}
            
            elif tool_name == "run_nurture_flow":
                result = call_api("/api/tasks/nurture-flow", "POST", {
                    "devices": _parse_devices(arguments.get("devices", "1")),
                    "ai_type": arguments.get("ai_type", "volc")
                })
                return {"jsonrpc": "2.0", "id": req.get("id"), "result": {"content": [{"type": "text", "text": str(result)}]}}
            
            elif tool_name == "run_reset_login":
                result = call_api("/api/tasks/reset-login", "POST", {
                    "devices": _parse_devices(arguments.get("devices", "1")),
                    "ai_type": arguments.get("ai_type", "volc")
                })
                return {"jsonrpc": "2.0", "id": req.get("id"), "result": {"content": [{"type": "text", "text": str(result)}]}}
            
            elif tool_name == "get_config":
                result = call_api("/api/config/")
                return {"jsonrpc": "2.0", "id": req.get("id"), "result": {"content": [{"type": "text", "text": str(result)}]}}
            
            elif tool_name == "set_host_ip":
                ip = arguments.get("ip")
                result = call_api(f"/api/config/host-ip?host_ip={ip}", "PUT")
                return {"jsonrpc": "2.0", "id": req.get("id"), "result": {"content": [{"type": "text", "text": str(result)}]}}
            
            elif tool_name == "list_devices":
                result = call_api("/api/devices/")
                return {"jsonrpc": "2.0", "id": req.get("id"), "result": {"content": [{"type": "text", "text": str(result)}]}}
            
            else:
                return {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}}
        
        else:
            return {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32600, "message": "Invalid Request"}}
    
    except Exception as e:
        return {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32603, "message": str(e)}}


def _parse_devices(dev_str: str) -> list:
    """解析设备字符串 '1-5' -> [1,2,3,4,5]"""
    devices = []
    for part in dev_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            devices.extend(range(int(start), int(end) + 1))
        else:
            devices.append(int(part))
    return sorted(devices)


def main():
    print("MYT MCP Server started (stdio mode)", file=sys.stderr)
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line.strip())
            resp = handle_request(req)
            print(json.dumps(resp))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
