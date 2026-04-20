# Progress Log

## Session: 2026-04-04

### Phase 1: 启动与定题

- **Status:** complete
- **Started:** 2026-04-04 15:58:50
- Actions taken:
  - 阅读课程 `README.md`
  - 修复并阅读 `03_fair_order_dispatch.md`
  - 提取 `rubric.xlsx` 的评分维度与权重
  - 确认该题目适合优先作为课程项目方向
- Files created/modified:
  - `fair_order_dispatch/README.md`
  - `fair_order_dispatch/task_plan.md`
  - `fair_order_dispatch/findings.md`
  - `fair_order_dispatch/progress.md`

### Phase 2: 设计锁定

- **Status:** complete
- Actions taken:
  - 固定区域级环境
  - 固定 `normal` 与 `shock` 两类场景
  - 固定效率、公平和辅助公平指标
  - 固定主奖励形式和 alpha 分析范围
- Files created/modified:
  - `fair_order_dispatch/task_plan.md`
  - `fair_order_dispatch/findings.md`

### Phase 3: 原型实现

- **Status:** complete
- Actions taken:
  - 搭建 `src/`、`scripts/`、`tests/`、`notebooks/`
  - 实现环境、指标、基线与 PPO 辅助代码
  - 将原型代码从仓库根目录整体迁移到 `fair_order_dispatch/`
  - 修正 Python 3.9.8 兼容性与本地运行路径
- Files created/modified:
  - `fair_order_dispatch/src/...`
  - `fair_order_dispatch/scripts/...`
  - `fair_order_dispatch/tests/...`
  - `fair_order_dispatch/pyproject.toml`
  - `fair_order_dispatch/.gitignore`

### Phase 4: 实验与结果整合

- **Status:** complete
- Actions taken:
  - 运行 baseline 评估
  - 生成 shock calibration 结果
  - 生成 baseline / PPO 结果表
  - 生成 4 张核心图
  - 确定当前主叙事采用 `alpha = 0.2`
- Files created/modified:
  - `fair_order_dispatch/results/baseline_results.csv`
  - `fair_order_dispatch/results/ppo_results.csv`
  - `fair_order_dispatch/results/shock_calibration.json`
  - `fair_order_dispatch/figures/episode_revenue_by_scene.png`
  - `fair_order_dispatch/figures/final_gini_by_scene.png`
  - `fair_order_dispatch/figures/shock_income_cdf.png`
  - `fair_order_dispatch/figures/alpha_tradeoff.png`

### Phase 5: 提交前 notebook 整理

- **Status:** in_progress
- Actions taken:
  - 先生成英文/骨架版 notebook
  - 再整理为中文 notebook
  - 将中文 notebook 升级为“自包含版”，内含关键代码、解释与结果
  - 为 notebook 交付增加测试，确保不是占位骨架
  - 更新记录文件，写清当前进度与下一步
- Files created/modified:
  - `fair_order_dispatch/final_submission_cn.ipynb`
  - `fair_order_dispatch/tests/test_notebook_deliverable.py`
  - `fair_order_dispatch/tests/test_chinese_notebook.py`
  - `fair_order_dispatch/README.md`
  - `fair_order_dispatch/task_plan.md`
  - `fair_order_dispatch/findings.md`
  - `fair_order_dispatch/progress.md`

## Test Results

| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| 项目测试集 | `python -m pytest -q` | 全部通过 | `22 passed in 0.22s` | pass |
| baseline 评估 | `python scripts/evaluate_baselines.py` | 正常输出结果表 | 写出 `4` 行 baseline 结果，并冻结 shock multiplier 为 `5` | pass |
| 中文 notebook 测试 | `python -m pytest -q tests/test_chinese_notebook.py` | notebook 存在、中文正常、自包含 | `3 passed` | pass |
| notebook 交付测试 | `python -m pytest -q tests/test_notebook_deliverable.py` | notebook 不再是占位骨架 | `2 passed` | pass |

## Error Log

| Timestamp | Error | Attempt | Resolution |
|-----------|-------|---------|------------|
| 2026-04-04 15:xx | proposal / 规划文档乱码 | 1 | 采用 UTF-8 / 安全重写方式修复 |
| 2026-04-04 16:xx | 本机 Python 不在 PATH 中 | 1 | 改用 Python 3.9.8 绝对路径 |
| 2026-04-04 17:xx | 根目录结构过乱 | 1 | 将所有实现迁移进 `fair_order_dispatch/` |
| 2026-04-04 19:xx | notebook 生成遇到 Windows 命令长度 / 路径问题 | 1 | 改用 Python 脚本重建 `.ipynb` |
| 2026-04-04 20:xx | 中文 notebook 出现乱码 | 1 | 使用 Unicode 安全方式重写 markdown 内容 |

## 5-Question Reboot Check

| Question | Answer |
|----------|--------|
| Where am I? | 当前处于 Phase 5：提交前 notebook 整理 |
| Where am I going? | 下一步是人工检查 `final_submission_cn.ipynb`，确认是否直接作为最终提交文件 |
| What's the goal? | 交付一个清晰、可解释、可提交的中文 notebook 作业文件 |
| What have I learned? | 当前故事线已经成立，关键是把 notebook 打磨成老师能顺畅阅读的形式 |
| What have I done? | 已完成原型实现、结果生成、目录收口和中文自包含 notebook |
