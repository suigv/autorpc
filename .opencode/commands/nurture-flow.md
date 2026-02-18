---
description: 养号流程
---

执行养号工作流：

## 触发词
"养号", "养号流程", "nurture", "维护"

## 参数
- 设备范围: $1 (如 "1-5" 或 "1,3,5")
- AI类型: $2 (volc=交友, part_time=兼职)

## 流程
1. 加载 skills.core.WorkflowEngine
2. 解析设备范围和 AI 类型
3. 对每个设备:
   - 抓取博主 (scrape)
4. 循环执行直到18点:
   - 养号互动 (nurture)
   - 私信回复 (dm)

## 示例
- "养号 1-5 volc"
- "养号流程 2,4 part_time"
- "维护 1-10 兼职"
