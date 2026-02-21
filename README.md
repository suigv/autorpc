# MYT RPA 自动化控制系统

支持 GUI、Web 与 API 的多设备自动化控制项目。

## 当前能力

- GUI 桌面控制台（Tkinter）
- FastAPI 接口（任务执行、停止、配置、数据管理）
- Web 控制台（`/web`）
  - 多设备下发命令
  - 任务详细日志（级别、设备、task_id、响应详情）
  - 日志筛选与分组
  - 运行中停止与初始化按钮
- 初始化能力
  - API: `POST /api/tasks/initialize`
  - 可清理任务执行产生的固化状态文件并停止任务

## 运行要求

- Python 3.10+
- 已安装项目依赖

```bash
pip install -r requirements.txt
```

可选环境变量（AI）：

```bash
export VOLC_API_KEY="your_volc_api_key"
export PART_TIME_API_KEY="your_part_time_api_key"
```

## 启动方式

### 1) GUI

```bash
python main.py
```

### 2) API + Web

```bash
MYT_ROOT_PATH=$(pwd) PYTHONPATH=$(pwd) python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Web 地址：`http://localhost:8000/web`

## Debian 服务器一键部署（Web/API 专用）

服务器专用分支：`web-api-only`

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/suigv/autorpc/web-api-only/install_debian_webapi.sh)"
```

部署细节与可选参数见：`DEPLOY_WEB_API.md`

## 常用 API

```bash
# 健康检查
curl http://localhost:8000/health

# 配置读取
curl http://localhost:8000/api/config/

# 执行命令
curl -X POST http://localhost:8000/api/tasks/execute \
  -H "Content-Type: application/json" \
  -d '{"command":"养号 交友 4","device":4}'

# 停止单设备
curl -X POST http://localhost:8000/api/tasks/stop/4

# 拉取任务日志
curl "http://localhost:8000/api/tasks/logs?device_index=4&since_id=0&limit=120"

# 初始化（清理固化状态）
curl -X POST http://localhost:8000/api/tasks/initialize
```

## 任务说明（命令驱动）

常见命令关键字：

- `全套` / `full` -> 完整流程
- `养号` / `nurture` -> 养号流程
- `重置` / `reset` -> 一键新机
- `登录` / `login` -> 自动登录
- `仿冒` / `clone` -> 仿冒资料
- `关注` / `follow` -> 关注截流
- `私信` / `dm` -> 私信回复

AI 类型：

- `交友` -> `volc`
- `兼职` -> `part_time`

## 目录结构

```text
demo_py_x64/
├── app/                # FastAPI 应用
│   ├── api/            # 路由
│   ├── core/           # 引擎/设备/日志核心
│   └── models/         # 数据模型
├── common/             # 公共模块
├── tasks/              # 任务实现
├── web/                # 前端控制台
├── config/             # 配置
└── main.py             # GUI 主程序
```
