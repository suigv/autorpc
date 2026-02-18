---
description: 完整引流流程
---

执行完整工作流：

## 触发词
"全套", "完整流程", "跑全套", "引流", "full-flow"

## 参数
- 设备范围: $1 (如 "1-5" 或 "1,3,5")
- AI类型: $2 (volc=交友, part_time=兼职)

## 流程
1. 加载 skills.core.WorkflowEngine
2. 解析设备范围和 AI 类型
3. 对每个设备并行执行完整流程:
   - 一键新机 (reset)
   - 自动登录 (login)
   - 抓取博主 (scrape)
   - 仿冒博主 (clone)
   - 关注粉丝 (follow)
4. 循环执行直到18点:
   - 养号互动 (nurture)
   - 私信回复 (dm)

## 示例
- "全套 1-5 volc"
- "完整流程 1,3,5 part_time"
- "跑全套设备3到5兼职"
