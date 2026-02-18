---
description: 重置登录
---

执行重置登录工作流：

## 触发词
"重置登录", "新机登录", "reset-login", "一键新机"

## 参数
- 设备范围: $1 (如 "1-5" 或 "1,3,5")
- AI类型: $2 (volc=交友, part_time=兼职)

## 流程
1. 加载 skills.core.WorkflowEngine
2. 解析设备范围和 AI 类型
3. 对每个设备并行执行:
   - 一键新机 (reset)
   - 自动登录 (login)

## 示例
- "重置登录 1-5 volc"
- "新机登录 1,3,5 part_time"
- "reset-login 1-10"
