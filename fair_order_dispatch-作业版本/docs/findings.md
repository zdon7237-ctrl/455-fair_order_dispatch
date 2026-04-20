# Findings & Decisions

## Requirements

- 用户希望先以 `03_fair_order_dispatch` 为当前主项目方向。
- 用户希望为该项目建立一个独立、整洁的专用目录。
- 用户希望当前进度和下一步行动能写进项目记录文件。
- 用户明确表示最后很可能只提交一个 `.ipynb`。
- 用户要求最终 notebook 使用中文版表述。
- 用户进一步要求最终 notebook 尽量包含“全部代码 + 解释 + 结果”，而不是只当展示壳。

## Research Findings

- 这个题目适合用 synthetic simulation 完成课程项目，不依赖真实平台数据。
- 主线不是“用了 RL”，而是“需求冲击下效率与公平是否存在张力，以及奖励设计能否缓解这种张力”。
- 区域级环境足以讲清楚故事线，而且实现复杂度明显低于订单级环境。
- `episode_revenue` 适合作为主效率指标，`final_episode_gini` 适合作为主公平指标。
- 仅看平均表现会削弱项目价值，因此补充 `bottom20` 收入指标是有必要的。
- 在当前实验结果中，shock multiplier 经过校准后冻结为 `5`，这比初始设定 `3` 更能拉开场景差异。
- 当前结果里，`alpha = 0.2` 的 PPO 版本是最适合作为主叙事的配置。

## Current Status

- 已有独立项目目录 [fair_order_dispatch](D:/111_temu_商品/ST455/2026-project-gaogou/fair_order_dispatch)
- 已有 supporting code：
  - [src](D:/111_temu_商品/ST455/2026-project-gaogou/fair_order_dispatch/src)
  - [scripts](D:/111_temu_商品/ST455/2026-project-gaogou/fair_order_dispatch/scripts)
  - [tests](D:/111_temu_商品/ST455/2026-project-gaogou/fair_order_dispatch/tests)
- 已有结果与图：
  - [results](D:/111_temu_商品/ST455/2026-project-gaogou/fair_order_dispatch/results)
  - [figures](D:/111_temu_商品/ST455/2026-project-gaogou/fair_order_dispatch/figures)
- 已有主要交付文件：
  - [final_submission_cn.ipynb](D:/111_temu_商品/ST455/2026-project-gaogou/fair_order_dispatch/final_submission_cn.ipynb)
- 当前测试状态：`22 passed`

## Technical Decisions

| Decision | Rationale |
|----------|-----------|
| 将所有实现收口到 `fair_order_dispatch/` 下 | 防止仓库根目录变乱，也方便未来单独保留或删除 |
| 主提交物采用中文 notebook | 与用户最后可能只交 `.ipynb` 的需求一致 |
| 最终 notebook 改为自包含 | 单文件提交时不依赖本地模块也能看懂主体内容 |
| 保留 supporting code 和 tests | 方便后续修改、验证和复现 |
| 使用 Python 3.9.8 作为当前本机主环境 | 用户确认这是最常用版本，且已验证可用 |

## Issues Encountered

| Issue | Resolution |
|-------|------------|
| 原始记录文件出现乱码 | 重写为干净的 UTF-8 中文文档 |
| Python 虽已安装但终端中不可直接调用 | 使用绝对路径调用 Python 3.9.8 |
| 根目录结构一度过乱 | 已经重组到 `fair_order_dispatch/` 独立目录内 |
| 中文 notebook 一度不是自包含 | 已改为包含关键代码、解释和结果数据 |

## Resources

- 课程说明：[README.md](D:/111_temu_商品/ST455/2026-project-gaogou/README.md)
- 提案文件：[03_fair_order_dispatch.md](D:/111_temu_商品/ST455/2026-project-gaogou/docs/proposals/03_fair_order_dispatch.md)
- 项目子目录说明：[fair_order_dispatch/README.md](D:/111_temu_商品/ST455/2026-project-gaogou/fair_order_dispatch/README.md)
- 当前计划：[task_plan.md](D:/111_temu_商品/ST455/2026-project-gaogou/fair_order_dispatch/task_plan.md)
- 当前进度：[progress.md](D:/111_temu_商品/ST455/2026-project-gaogou/fair_order_dispatch/progress.md)
- 最终中文 notebook：[final_submission_cn.ipynb](D:/111_temu_商品/ST455/2026-project-gaogou/fair_order_dispatch/final_submission_cn.ipynb)

## Visual / Result Findings

- `Local-First` 在当前实验里拿到了最高的 revenue，但公平性不是最优。
- `Demand-Greedy` 在当前实验里效率与公平都较差。
- `PPO (alpha = 0.2)` 在 shock 场景下显著降低了 Gini，并抬高了 bottom 20% 司机收入。
- 当前 notebook 已经可以支持“效率与公平存在张力，但奖励设计可以缓解冲突”这一结论。
