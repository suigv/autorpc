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

### 1. GUI 桌面应用
```bash
cd demo_py_x64
/usr/bin/python3 main.py
```

### 2. REST API 服务
```bash
cd demo_py_x64

# 安装依赖
pip3 install --break-system-packages -r requirements.txt
pip3 install websockets uvicorn[standard] --break-system-packages

# 启动服务（必须设置环境变量）
MYT_ROOT_PATH=$(pwd) PYTHONPATH=$(pwd) uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Web 前端控制台
启动API服务后访问：**http://localhost:8000/web**

功能：
- 设备多选（复选框）
- 实时日志显示
- 发送指令执行任务
- 编辑账号/位置/网站配置

### 4. MCP 服务 (需先启动 API)
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

# 执行任务（支持自然语言）
curl -X POST http://localhost:8000/api/tasks/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "养号 3 volc"}'
```

### 方式三：Web 前端

访问 http://localhost:8000/web
- 选择设备（多选）
- 输入指令：养号、全套、重置、关注、私信等
- 实时查看日志

### 方式四：OpenCode Skills

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

### 数据管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/data/accounts` | 获取账号列表 |
| PUT | `/api/data/accounts` | 更新账号列表 |
| GET | `/api/data/location` | 获取位置列表 |
| PUT | `/api/data/location` | 更新位置列表 |
| GET | `/api/data/website` | 获取网站列表 |
| PUT | `/api/data/website` | 更新网站列表 |

### 任务执行

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/tasks/execute` | 执行任务（自然语言） |

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

### 数据文件格式

| 文件 | 格式 | 说明 |
|------|------|------|
| 账号.txt | 用户名----密码----2FA密钥 | 每行一个账号 |
| 位置.txt | 每行一个位置 | volc用第1行，part_time用第2行 |
| 网页.txt | 每行一个网址 | volc用第1行，part_time用第2行 |

---

## 任务类型

| 类型 | 说明 |
|------|------|
| full_flow | 完整流程 (一键新机→自动登录→抓博主→仿冒→关注截流→智能养号→主页互动→引用截流→私信回复→循环) |
| nurture_flow | 养号流程 (抓博主→循环:关注截流→智能养号→主页互动→引用截流→私信回复) |
| reset_login | 重置登录 (一键新机+自动登录) |

## GUI 任务选项

| 任务 | 说明 | 主流程 | 循环 |
|------|------|--------|------|
| 一键新机 | 软重启应用并清除数据 | ✅ | - |
| 自动登录 | 支持2FA验证 | ✅ | - |
| 仿冒博主 | 克隆目标博主头像、banner、个人资料 | ✅ | - |
| 关注截流 | 跳转博主粉丝页随机关注 | ✅ | ✅ |
| 私信回复 | AI自动回复私信 | ✅ | ✅ |
| 智能养号 | 搜索关键词浏览点赞互动 | ✅ | ✅ |
| 主页互动 | 首页随机点赞互动 | ✅ | ✅ |
| 引用截流 | 自动评论引流 | ✅ | ✅ |

---

## 注意事项

1. 设备离线时任务返回 `false`，但不报错
2. API 服务需启动才能使用 MCP
3. GUI 和 API 可以同时运行，互不干扰
