# MYT Skills

> RPA 工作流自动化模块

## 目录结构

```
demo_py_x64/
├── skills/                 # Skills 模块
│   ├── __init__.py
│   ├── __main__.py       # CLI 入口
│   ├── core/             # 核心模块
│   │   ├── config_loader.py    # 配置加载
│   │   ├── port_calc.py        # 端口计算
│   │   ├── device_manager.py   # 设备管理
│   │   └── workflow_engine.py # 工作流引擎
│   └── tasks/            # 任务脚本(可选)
│
├── config/
│   └── devices.json      # 设备配置
│
└── tasks/               # 原有 task 任务
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方式

### CLI 命令

```bash
# 完整流程 (重置→登录→抓取→仿冒→关注→养号循环)
python -m skills run full 1-5 volc
python -m skills run full 1-5 part_time

# 养号流程 (抓取→养号循环)
python -m skills run nurture 1-5 volc

# 重置登录
python -m skills run reset 1-10 volc

# 单独抓取博主
python -m skills scrape 1 volc
python -m skills scrape 2 part_time

# 配置管理
python -m skills config show              # 显示配置
python -m skills config ip 192.168.1.xxx  # 修改IP
```

### Python 代码调用

```python
from skills.core import WorkflowEngine, parse_device_range, parse_ai_type

engine = WorkflowEngine()

# 完整流程
engine.run_full_flow([1, 2, 3], "volc")

# 养号流程
engine.run_nurture_flow([1, 2], "part_time")

# 重置登录
engine.run_reset_login([1], "volc")
```

## 配置

编辑 `config/devices.json`:

```json
{
  "host_ip": "192.168.1.215",
  "total_devices": 10,
  "default_ai": "volc",
  "stop_hour": 18,
  "cycle_interval": 15
}
```

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| host_ip | 设备 IP | 192.168.1.215 |
| total_devices | 设备数量 | 10 |
| default_ai | 默认AI类型 | volc |
| stop_hour | 停止时间(小时) | 18 |
| cycle_interval | 循环间隔(秒) | 15 |

## 设备格式

- 连续: `1-5` → 设备 1,2,3,4,5
- 分散: `1,3,5` → 设备 1,3,5
- 混合: `1-3,5,7-9` → 设备 1,2,3,5,7,8,9

## AI 类型

- `volc` - 交友接口
- `part_time` - 兼职接口
