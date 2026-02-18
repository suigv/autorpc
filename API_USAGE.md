# AutoRPC API 使用指南

## 基础信息

- **Base URL**: `http://localhost:8000`
- **API 文档**: `http://localhost:8000/docs`

---

## 目录

1. [配置管理](#配置管理)
2. [设备管理](#设备管理)
3. [任务管理](#任务管理)
4. [完整示例](#完整示例)

---

## 配置管理

### 获取全部配置

```bash
curl http://localhost:8000/api/config/
```

**响应:**
```json
{
  "host_ip": "192.168.1.215",
  "total_devices": 10,
  "default_ai": "volc",
  "stop_hour": 18,
  "cycle_interval": 15
}
```

### 获取设备 IP

```bash
curl http://localhost:8000/api/config/host-ip
```

**响应:**
```json
{"host_ip": "192.168.1.215"}
```

### 修改设备 IP

```bash
curl -X PUT "http://localhost:8000/api/config/host-ip?host_ip=192.168.1.100"
```

**响应:**
```json
{"host_ip": "192.168.1.100", "status": "updated"}
```

### 批量更新配置

```bash
curl -X PUT http://localhost:8000/api/config/ \
  -H "Content-Type: application/json" \
  -d '{
    "stop_hour": 20,
    "cycle_interval": 30,
    "default_ai": "part_time"
  }'
```

---

## 设备管理

### 列出所有设备

```bash
curl http://localhost:8000/api/devices/
```

**响应:**
```json
[
  {
    "index": 1,
    "ip": "192.168.1.215",
    "rpa_port": 30002,
    "api_port": 30001,
    "ai_type": "volc",
    "status": "idle"
  }
]
```

### 获取单个设备详情

```bash
curl http://localhost:8000/api/devices/1
```

### 获取设备状态

```bash
curl http://localhost:8000/api/devices/1/status
```

**响应:**
```json
{
  "index": 1,
  "status": "idle",
  "current_task": null,
  "message": null
}
```

### 启动单设备任务

```bash
# 完整流程
curl -X POST "http://localhost:8000/api/devices/1/start?task_type=full_flow&ai_type=volc"

# 养号流程
curl -X POST "http://localhost:8000/api/devices/1/start?task_type=nurture_flow&ai_type=part_time"

# 重置登录
curl -X POST "http://localhost:8000/api/devices/1/start?task_type=reset_login&ai_type=volc"
```

**响应:**
```json
{
  "device_id": 1,
  "status": "started",
  "result": {"total": 1, "results": {"1": false}}
}
```

### 停止单设备任务

```bash
curl -X POST http://localhost:8000/api/devices/1/stop
```

**响应:**
```json
{"device_id": 1, "status": "stopped"}
```

### 批量启动设备

```bash
# 设备范围: 1-5
curl -X POST "http://localhost:8000/api/devices/batch/start?devices=1-5&task_type=full_flow&ai_type=volc"

# 设备列表: 1,3,5
curl -X POST "http://localhost:8000/api/devices/batch/start?devices=1,3,5&task_type=nurture_flow&ai_type=part_time"

# 混合: 1-3 和 5
curl -X POST "http://localhost:8000/api/devices/batch/start?devices=1-3,5&task_type=reset_login&ai_type=volc"
```

**响应:**
```json
{
  "devices": [1, 2, 3, 4, 5],
  "status": "started",
  "result": {"total": 5, "results": {"1": false, "2": false, "3": false, "4": false, "5": false}}
}
```

### 批量停止设备

```bash
curl -X POST http://localhost:8000/api/devices/batch/stop
```

**响应:**
```json
{"status": "all_stopped"}
```

---

## 任务管理

### 创建完整流程任务

```bash
curl -X POST http://localhost:8000/api/tasks/full-flow \
  -H "Content-Type: application/json" \
  -d '{
    "devices": [1, 2, 3, 4, 5],
    "ai_type": "volc"
  }'
```

### 创建养号任务

```bash
curl -X POST http://localhost:8000/api/tasks/nurture-flow \
  -H "Content-Type: application/json" \
  -d '{
    "devices": [1, 2],
    "ai_type": "part_time"
  }'
```

### 创建重置登录任务

```bash
curl -X POST http://localhost:8000/api/tasks/reset-login \
  -H "Content-Type: application/json" \
  -d '{
    "devices": [1],
    "ai_type": "volc"
  }'
```

**任务响应 (通用):**
```json
{
  "task_id": "14fae991",
  "task_type": "full_flow",
  "devices": [1, 2],
  "ai_type": "volc",
  "status": "running",
  "created_at": "2026-02-19T00:04:01.809811"
}
```

### 获取任务列表

```bash
# 所有任务
curl http://localhost:8000/api/tasks/

# 最近 10 个
curl "http://localhost:8000/api/tasks/?limit=10"
```

**响应:**
```json
[
  {
    "task_id": "14fae991",
    "task_type": "full_flow",
    "devices": [1, 2],
    "ai_type": "volc",
    "status": "completed",
    "created_at": "2026-02-19T00:04:01.809811"
  }
]
```

### 获取任务详情

```bash
curl http://localhost:8000/api/tasks/14fae991
```

**响应:**
```json
{
  "task_id": "14fae991",
  "task_type": "full_flow",
  "devices": [1, 2],
  "ai_type": "volc",
  "status": "completed",
  "created_at": "2026-02-19T00:04:01.809811",
  "result": {
    "total": 2,
    "results": {"1": false, "2": false}
  },
  "error": null
}
```

### 取消任务

```bash
curl -X POST http://localhost:8000/api/tasks/14fae991/cancel
```

**响应:**
```json
{"task_id": "14fae991", "status": "cancelled"}
```

---

## 完整示例

### 完整工作流示例

```bash
#!/bin/bash

# 1. 查看当前配置
echo "=== 当前配置 ==="
curl -s http://localhost:8000/api/config/
echo ""

# 2. 查看设备列表
echo "=== 设备列表 ==="
curl -s http://localhost:8000/api/devices/
echo ""

# 3. 启动设备 1-3 完整流程
echo "=== 启动完整流程 ==="
curl -s -X POST http://localhost:8000/api/tasks/full-flow \
  -H "Content-Type: application/json" \
  -d '{"devices": [1, 2, 3], "ai_type": "volc"}'
echo ""

# 4. 等待 3 秒后查看任务状态
sleep 3
echo "=== 任务状态 ==="
curl -s http://localhost:8000/api/tasks/ | head -c 500
echo ""
```

### Python 示例

```python
import requests

API_BASE = "http://localhost:8000"

# 获取配置
def get_config():
    r = requests.get(f"{API_BASE}/api/config/")
    return r.json()

# 修改 IP
def set_host_ip(ip):
    r = requests.put(f"{API_BASE}/api/config/host-ip?host_ip={ip}")
    return r.json()

# 获取设备列表
def list_devices():
    r = requests.get(f"{API_BASE}/api/devices/")
    return r.json()

# 启动任务
def start_task(task_type, devices, ai_type="volc"):
    r = requests.post(
        f"{API_BASE}/api/tasks/{task_type}",
        json={"devices": devices, "ai_type": ai_type}
    )
    return r.json()

# 获取任务状态
def get_task(task_id):
    r = requests.get(f"{API_BASE}/api/tasks/{task_id}")
    return r.json()

# 使用示例
if __name__ == "__main__":
    # 查看配置
    print(get_config())
    
    # 启动完整流程
    result = start_task("full-flow", [1, 2, 3], "volc")
    print(result)
    
    # 查看任务
    print(get_task(result["task_id"]))
```

### JavaScript/Node.js 示例

```javascript
const API_BASE = "http://localhost:8000";

async function apiCall(endpoint, method = "GET", body = null) {
    const options = { method, headers: { "Content-Type": "application/json" } };
    if (body) options.body = JSON.stringify(body);
    const res = await fetch(`${API_BASE}${endpoint}`, options);
    return res.json();
}

// 获取配置
console.log(await apiCall("/api/config/"));

// 启动任务
console.log(await apiCall("/api/tasks/full-flow", "POST", {
    devices: [1, 2, 3],
    ai_type: "volc"
}));

// 批量启动
console.log(await apiCall("/api/devices/batch/start?devices=1-5&task_type=nurture_flow", "POST"));
```

---

## 任务类型说明

| task_type | 说明 |
|-----------|------|
| `full_flow` | 完整流程: 一键新机 → 自动登录 → 抓取博主 → 仿冒博主 → 关注粉丝 → 循环养号 |
| `nurture_flow` | 养号流程: 抓取博主 → 循环养号 → 私信回复 |
| `reset_login` | 重置登录: 一键新机 → 自动登录 |

## AI 类型说明

| ai_type | 说明 |
|---------|------|
| `volc` | 交友接口 |
| `part_time` | 兼职接口 |

## 设备状态说明

| status | 说明 |
|--------|------|
| `idle` | 空闲 |
| `running` | 运行中 |
| `offline` | 离线 |
| `error` | 错误 |

## 任务状态说明

| status | 说明 |
|--------|------|
| `pending` | 待执行 |
| `running` | 执行中 |
| `completed` | 已完成 |
| `failed` | 失败 |
| `cancelled` | 已取消 |
