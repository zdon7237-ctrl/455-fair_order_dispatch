# Fair Order Dispatch 修改日志

本文件记录项目的所有重要修改，方便新的 Claude 会话接手工作。

---

## 2026-04-05

### 已完成
- **整合 Colab 实验结果**
  - 复制多种子实验结果文件到 `results/` 文件夹
    - `multi_seed_results.csv` - 60行原始数据（5种子×12算法组合）
    - `statistical_summary.csv` - 统计汇总（均值、标准差、标准误）
    - `significance_tests.csv` - 显著性检验（t检验、p值、Cohen's d）
  - 复制图表到 `figures/` 文件夹
    - `alpha_tradeoff.png` - 带误差棒的效率-公平权衡图
    - `episode_revenue_by_scene.png` - 带误差棒的收益对比图
    - `final_gini_by_scene.png` - 带误差棒的公平性对比图
  - 备份旧的单次实验结果（重命名为 `*_old.*`）

- **更新 final_submission_cn.ipynb**
  - Cell 7：修改为从 `statistical_summary.csv` 读取多种子实验结果
    - 构建 baseline_records 和 ppo_records，格式化为 "均值±标准差"
    - 保留 shock_income_samples（用于 CDF 图）
  - Cell 6：更新 Markdown 表格为均值±标准差格式
    - 添加说明：多种子实验结果（n=5，种子=[0, 42, 123, 456, 789]）
    - 添加统计显著性说明（p值）
  - Cell 9：为图表添加误差棒
    - 图表1-2：使用 `yerr` 参数添加误差棒
    - 图表3：保持单次实验的 CDF 图（CDF 不适合误差棒）
    - 图表4：使用 `errorbar` 添加 x 和 y 方向的误差棒
  - 添加小组贡献说明部分（新 Cell，在参考文献之后）
    - 包含占位符，提醒用户填写具体成员信息

- **更新追踪文件**
  - 更新 CHANGELOG.md（本文件）
  - 更新 PROGRESS.md
  - 更新 PLAN.md

### 实验结果摘要
- **实验规模**：
  - 5个种子：[0, 42, 123, 456, 789]
  - 60个实验：2 baselines × 2 scenes × 5 seeds + PPO × 2 scenes × 4 alphas × 5 seeds
  - 统计方法：t检验、Cohen's d 效应量

- **关键发现**：
  - **PPO(α=0.2) vs Demand-Greedy**：
    - 平台收入：+242.7% (1207.6 vs 352.4, p<0.001) ⭐ 显著
    - 基尼系数：-54.6% (0.0912 vs 0.2008, p<0.001) ⭐ 显著
  - **PPO(α=0.2) vs Local-First**：
    - 平台收入（normal）：-2.2% (1207.6 vs 1234.6, p=0.206) - 无显著差异
    - 基尼系数（shock）：-27.8% (0.0842 vs 0.1166, p=0.003) ⭐ 显著更公平

### 技术说明
- 所有图表已更新为带误差棒的版本
- Notebook 现在可以从 CSV 文件读取多种子实验结果
- 保留了单次实验的 CDF 图（因为 CDF 不适合显示误差棒）

---

## 2026-04-04

### 新增
- 创建团队 `fair-dispatch-improvement`
- 创建进度追踪文件系统：
  - `PROGRESS.md` - 每日进度追踪
  - `PLAN.md` - 详细执行计划
  - `CHANGELOG.md` - 修改日志（本文件）
- 制定三阶段改进计划（课程作业 → 会议论文 → SCI 期刊）

### 已完成
- **补充参考文献到8条**（doc-writer 完成）
  - 更新文件：
    - `notebooks/fair_order_dispatch_report.ipynb` Cell 11
    - `final_submission_cn.ipynb` Cell 11
  - 引用格式：APA 格式，包含完整作者、年份、标题、会议/期刊信息
  - 新增参考文献：
    1. Schulman et al. (2017) - PPO 算法原始论文
    2. Xu et al. (2018) - 滴滴大规模订单派单
    3. Tang et al. (2019) - 深度价值网络派单
    4. Qin et al. (2020) - 异构动作空间强化模仿学习
    5. Zheng et al. (2021) - 公平感知订单派单
    6. Shi et al. (2022) - A/B 测试中的动态因果效应
    7. Wang et al. (2022) - 长期效率与公平优化
    8. Li et al. (2024) - 基于强化学习的公平动态匹配
- **创建 requirements.txt**
  - 列出所有项目依赖及版本要求
- **修复 notebook 编码问题**（notebook-fixer 完成）
  - 修复文件：`final_submission_cn.ipynb`
  - 修复内容：
    - Cell 3：修复 `_load_ppo` 函数错误提示（??? → 请先安装 stable-baselines3 才能在 notebook 中使用 PPO）
    - Cell 7：修复 print 语句（???????? → 最终冲击倍数）
    - Cell 9：修复4个图表标题的中文编码
      - `?????? episode_revenue` → `不同场景下的 episode_revenue`
      - `?????? final_episode_gini` → `不同场景下的 final_episode_gini`
      - `??????????? CDF` → `冲击场景下司机收入分布 CDF`
      - `alpha ???????-????` → `alpha 参数的效率-公平权衡`
    - Cell 9：添加 matplotlib 中文字体配置（Microsoft YaHei, SimHei）
    - Cell 0：优化摘要格式（`6` → 6个，`60` → 60名，`40` → 40个）

### 计划
- 补充多种子统计分析（5个种子）
- 添加小组贡献说明

### 技术说明
- 硬件环境：AMD 显卡，使用 CPU 版本 PyTorch
- 所有代码和注释使用中文
- Python 3.9.8

---

## 历史记录（2026-04-04 之前）

### 已完成
- Phase 1-4：项目原型实现
- 基础实验：2个 baseline + PPO（4个 alpha 值）
- 生成4张核心图表
- 创建中文自包含 notebook
- 测试通过：22 passed

### 当前问题
- notebook 中有5处中文编码损坏
- 所有实验都是单次运行（seed=0）
- 缺少统计显著性检验
- 参考文献仅3条

---

## 待办事项

### 高优先级 🔴
- [ ] 修复编码问题
- [ ] 运行多种子实验
- [ ] 统计分析

### 中优先级 🟠
- [ ] 补充参考文献

### 低优先级 🟡
- [ ] 添加小组贡献说明

---

更新日期：2026-04-04
