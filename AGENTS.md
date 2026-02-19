# MYT RPA 使用指南

## 概述

MYT RPA 自动化系统，支持四种使用方式：
1. **GUI 桌面应用** - Tkinter 图形界面
2. **REST API** - HTTP 接口
3. **Skills** - OpenCode 自然语言触发
4. **MCP** - AI 模型调用

## 目录结构

```
demo_py_x64/
├── app/                    # FastAPI 主应用
│   ├── main.py            # 应用入口
│   ├── api/               # API 路由
│   │   ├── devices.py     # 设备管理
│   │   ├── tasks.py       # 任务调度
│   │   └── config.py      # 配置管理
│   └── core/              # 核心服务
│
├── mcp_server.py          # MCP 服务器
├── mcp_config.json        # MCP 配置
├── main.py               # GUI 桌面应用 (保留)
├── skills/               # 原 Python 模块
├── tasks/                # 任务实现
├── common/               # 公共模块
└── config/
    └── devices.json      # 配置文件
```

---

## 启动方式

### 1. GUI 桌面应用 (原有)
```bash
python main.py
```

### 2. REST API 服务
```bash
# 安装依赖
pip3 install --break-system-packages -r requirements.txt

# 启动服务
cd demo_py_x64
PYTHONPATH=$(pwd) uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. MCP 服务 (需先启动 API)
```bash
# 方式一：直接运行
python3 mcp_server.py

# 方式二：配置到 Claude Desktop
# 将 mcp_config.json 内容添加到 Claude Desktop 的 MCP 配置中
```

---

## 使用方式

### 方式一：GUI 桌面应用
原有 Tkinter 界面，完全保留，功能不变。

### 方式二：REST API

```bash
# 查看配置
curl http://localhost:8000/api/config/

# 修改 IP
curl -X PUT "http://localhost:8000/api/config/host-ip?host_ip=192.168.1.100"

# 创建完整流程任务
curl -X POST http://localhost:8000/api/tasks/full-flow \
  -H "Content-Type: application/json" \
  -d '{"devices": [1,2,3], "ai_type": "volc"}'

# 批量启动
curl -X POST "http://localhost:8000/api/devices/batch/start?devices=1-5&task_type=nurture_flow"
```

### 方式三：OpenCode Skills

在 OpenCode 中直接说话触发：

| 触发词 | 功能 |
|--------|------|
| "全套 1-5 volc" | 设备1-5完整流程 |
| "养号 2,4 part_time" | 设备2,4养号流程 |
| "重置登录 1-10 volc" | 设备1-10重置登录 |

### 方式四：MCP

配置到 Claude Desktop 后，可直接对话：
- "运行设备1-3的完整流程"
- "查看当前配置"
- "设置设备IP为192.168.1.100"

---

## API 接口文档

### 配置管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/config/` | 获取全部配置 |
| PUT | `/api/config/host-ip?host_ip=xxx` | 修改设备 IP |

### 设备管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/devices/` | 列出所有设备 |
| GET | `/api/devices/{id}/status` | 获取设备状态 |
| POST | `/api/devices/{id}/start?task_type=xxx` | 启动设备任务 |
| POST | `/api/devices/batch/start?devices=1-5` | 批量启动 |

### 任务管理

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/tasks/full-flow` | 完整流程 |
| POST | `/api/tasks/nurture-flow` | 养号流程 |
| POST | `/api/tasks/reset-login` | 重置登录 |
| GET | `/api/tasks/` | 任务列表 |
| GET | `/api/tasks/{task_id}` | 任务详情 |

---

## Python 代码调用

```python
import sys
sys.path.insert(0, 'demo_py_x64')

from app.core.workflow_engine import WorkflowEngine
from app.core.device_manager import parse_device_range

engine = WorkflowEngine()

# 完整流程
engine.run_full_flow([1,2,3,4,5], "volc")

# 养号流程
engine.run_nurture_flow([2,4], "part_time")

# 重置登录
engine.run_reset_login([1], "volc")
```

---

## 配置说明

编辑 `config/devices.json`:

| 参数 | 说明 | 示例 |
|------|------|------|
| host_ip | 设备主机 IP | "192.168.1.215" |
| total_devices | 设备总数 | 10 |
| default_ai | 默认 AI 类型 | "volc" |
| stop_hour | 停止时间 (小时) | 18 |
| cycle_interval | 循环间隔 (秒) | 15 |

---

## 任务类型

| 类型 | 说明 |
|------|------|
| full_flow | 完整流程 (新机->登录->抓博主->仿冒->关注->私信->循环:养号->主页互动->引用截流->私信回复) |
| nurture_flow | 养号流程 (抓博主->循环:养号->主页互动->引用截流->私信回复) |
| reset_login | 重置登录 (新机->登录) |

## GUI 任务选项

| 任务 | 说明 |
|------|------|
| 一键新机 | 软重启应用并清除数据 |
| 自动登录 | 支持2FA验证 |
| 仿冒博主 | 克隆目标博主头像、banner、个人资料 |
| 关注截流 | 跳转博主粉丝页随机关注 |
| 私信回复 | AI自动回复私信 |
| 智能养号 | 搜索关键词浏览点赞互动 |
| 主页互动 | 首页随机点赞互动 |
| 引用截流 | 自动评论引流 |

---

## 注意事项

1. 设备离线时任务返回 `false`，但不报错
2. API 服务需启动才能使用 MCP
3. GUI 和 API 可以同时运行，互不干扰
