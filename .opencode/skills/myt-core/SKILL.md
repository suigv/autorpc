---
name: myt-core
description: |
  MYT RPA 核心 - 提供工作流引擎、配置管理
  
  始终自动加载
管理、设备---

## 核心功能

### 导入模块
```python
import sys
sys.path.insert(0, 'demo_py_x64')

from app.core.workflow_engine import WorkflowEngine
from app.core.device_manager import parse_device_range, parse_ai_type
from app.core.config_loader import get_host_ip, get_total_devices, get_stop_hour, get_cycle_interval, update_host_ip
```

### 使用示例
```python
# 创建工作流引擎
engine = WorkflowEngine()

# 运行完整流程 (设备1-5, 交友AI)
engine.run_full_flow([1,2,3,4,5], "volc")

# 运行养号流程 (设备2,4, 兼职AI)
engine.run_nurture_flow([2,4], "part_time")

# 运行重置登录 (设备1-10)
engine.run_reset_login([1,2,3,4,5,6,7,8,9,10], "volc")
```

### 配置管理
```python
# 获取配置
get_host_ip()        # 设备IP
get_total_devices()  # 设备数量
get_stop_hour()     # 停止时间

# 修改配置
update_host_ip("192.168.1.xxx")  # 更新设备IP
```

### 设备解析
```python
# 解析设备字符串 "1-5" -> [1,2,3,4,5]
devices = parse_device_range("1-5")

# 解析AI类型
ai_type = parse_ai_type("volc")  # -> "volc"
ai_type = parse_ai_type("兼职")   # -> "part_time"
```

## 触发词

| 触发词 | 功能 |
|--------|------|
| "全套 1-5 volc" | 设备1-5完整流程 |
| "养号 2,4 part_time" | 设备2,4养号流程 |
| "重置登录 1-10 volc" | 设备1-10重置登录 |
