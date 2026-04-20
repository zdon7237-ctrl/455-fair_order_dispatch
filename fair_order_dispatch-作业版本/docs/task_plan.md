# Task Plan: Fair Order Dispatch

## Goal

完成一个围绕“需求冲击下订单派单的效率与公平权衡”的课程项目原型，并整理出一个可单独提交的中文 notebook 交付物。

## Current Phase

Phase 5: 提交前润色与确认

## Phases

### Phase 1: 启动与定题

- [x] 阅读课程 README
- [x] 阅读 `03_fair_order_dispatch` 提案
- [x] 提取 rubric 评分重点
- [x] 建立独立子项目目录 `fair_order_dispatch/`
- **Status:** complete

### Phase 2: 设计锁定

- [x] 固定区域级环境
- [x] 固定主公平指标为 `final_episode_gini`
- [x] 固定辅助公平指标为 `final_episode_bottom20_income_mean`
- [x] 固定 `normal` 与 `shock` 两类场景
- [x] 固定奖励形式 `completion_rate - alpha * gini`
- **Status:** complete

### Phase 3: 原型实现

- [x] 实现环境、指标、基线和 PPO 辅助代码
- [x] 建立 `src/`、`scripts/`、`tests/`、`notebooks/` 结构
- [x] 把所有实现收口到 `fair_order_dispatch/` 目录内
- [x] 兼容本机 Python 3.9.8 环境
- **Status:** complete

### Phase 4: 实验与结果整合

- [x] 生成 baseline 结果表
- [x] 生成 PPO 结果表
- [x] 冻结 shock multiplier 为 `5`
- [x] 生成 4 张核心图
- [x] 整理中文 notebook 的主结果表和结论
- **Status:** complete

### Phase 5: 提交前润色与确认

- [x] 生成中文最终 notebook `final_submission_cn.ipynb`
- [x] 将 notebook 做成“代码 + 解释 + 结果”自包含版本
- [x] 通过当前测试集验证
- [ ] 在 Jupyter 中手动打开并 `Run All`
- [ ] 检查摘要、结论和参考文献格式是否符合老师习惯
- [ ] 确认最终是否只提交这一个 `.ipynb`
- [ ] 如有需要，将文件重命名为更直接的提交文件名
- **Status:** in_progress

## Key Questions

1. 最终是否只提交一个 notebook，而不额外提交 `src/`、`scripts/` 等辅助目录？
2. 当前 notebook 的中文叙述是否已经足够像正式课程作业，而不只是项目说明？
3. 是否需要在提交前把 PPO 训练预算调大，还是当前原型结果已经足够支撑故事线？

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| 使用 `fair_order_dispatch/` 作为独立子项目目录 | 避免把课程仓库根目录弄乱，后续即使不用这个题目也容易单独处理 |
| 采用区域级环境而不是订单级环境 | 更容易在课程项目时间内完成完整闭环 |
| 将主交付物收口为中文 notebook | 用户明确提出最后可能只交 `.ipynb` |
| 使用 `final_submission_cn.ipynb` 作为当前主交付文件 | 便于直接检查和提交 |
| notebook 改为“自包含版” | 即使只上传 notebook，也能同时包含代码、解释和结果 |
| 维持 supporting code 在 `src/`、`scripts/`、`tests/` 中 | 方便后续维护、复现和扩展，不影响 notebook 单文件提交 |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| 初次读取 proposal 和规划文件出现乱码 | 1 | 重新按 UTF-8/安全方式写入并重建文档 |
| 本机 Python 不在 PATH 中 | 1 | 直接使用 `C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python39\\python.exe` |
| 根目录结构被原型代码铺开，显得混乱 | 1 | 将实现全部移动进 `fair_order_dispatch/` |
| 生成 notebook 时命中 Windows 命令长度/路径问题 | 1 | 改为用 Python 脚本重写 `.ipynb` 文件 |
| 中文 notebook 一度出现乱码 | 1 | 用 Unicode 安全方式重写 markdown 内容 |

## Notes

- 当前原型已经达到“可以拿来继续润色成作业”的阶段。
- 当前最重要的下一步不是继续扩功能，而是打开 `final_submission_cn.ipynb` 做人工检查。
- 如果时间有限，优先保证：notebook 叙事顺畅、结果可见、引用规范。
