# Fair Order Dispatch - 项目文件结构说明

## 📁 项目组织

```
fair_order_dispatch/
│
├── 📄 final_submission_cn.ipynb    ⭐ 主要交付物（课程作业提交文件）
├── 📄 README.md                    📖 项目说明（本文件）
├── 📄 requirements.txt             📦 Python 依赖列表
├── 📄 pyproject.toml               ⚙️ 项目配置
│
├── 📂 docs/                        📚 项目文档
│   ├── PLAN.md                     详细执行计划（三阶段改进路线）
│   ├── CHANGELOG.md                修改日志（记录所有变更）
│   ├── PROGRESS.md                 当前进度追踪
│   ├── task_plan.md                任务计划（历史记录）
│   ├── findings.md                 研究发现和决策记录
│   └── progress_old.md             旧的进度记录（存档）
│
├── 📂 src/                         💻 源代码
│   └── fair_dispatch/
│       ├── __init__.py
│       ├── config.py               配置参数
│       ├── environment.py          仿真环境
│       ├── metrics.py              评价指标
│       ├── baselines.py            基线算法
│       └── rl_interface.py         强化学习接口
│
├── 📂 scripts/                     🔧 实验脚本
│   ├── evaluate_baselines.py      基线评估
│   ├── train_ppo.py                PPO 训练
│   ├── generate_plots.py          生成图表
│   ├── run_multi_seed_experiments.py  ⭐ 多种子实验（新）
│   └── statistical_analysis.py    ⭐ 统计分析（新）
│
├── 📂 tests/                       🧪 测试代码
│   ├── test_environment.py
│   ├── test_metrics.py
│   ├── test_baselines.py
│   └── test_notebook_deliverable.py
│
├── 📂 notebooks/                   📓 Notebook 草稿
│   └── fair_order_dispatch_report.ipynb
│
├── 📂 results/                     📊 实验结果
│   ├── baseline_results.csv       基线结果
│   ├── ppo_results.csv             PPO 结果
│   ├── shock_calibration.json      冲击校准
│   ├── multi_seed_results.csv      ⭐ 多种子结果（待生成）
│   ├── statistical_summary.csv     ⭐ 统计汇总（待生成）
│   └── significance_tests.csv      ⭐ 显著性检验（待生成）
│
└── 📂 figures/                     📈 图表
    ├── episode_revenue_by_scene.png
    ├── final_gini_by_scene.png
    ├── shock_income_cdf.png
    └── alpha_tradeoff.png
```

---

## ⭐ 重要文件标记

### 🔴 最重要（课程作业提交）
- **`final_submission_cn.ipynb`** - 最终提交的 notebook，包含所有代码、结果和说明

### 🟠 核心脚本（运行实验）
- **`scripts/run_multi_seed_experiments.py`** - 运行多种子实验（5个种子，60个实验）
- **`scripts/statistical_analysis.py`** - 统计分析和显著性检验

### 🟡 配置和依赖
- **`requirements.txt`** - 安装依赖：`pip install -r requirements.txt`
- **`src/fair_dispatch/config.py`** - 实验参数配置

### 🟢 文档（了解项目）
- **`docs/PLAN.md`** - 三阶段改进计划（作业→会议→期刊）
- **`docs/CHANGELOG.md`** - 所有修改记录
- **`docs/PROGRESS.md`** - 当前进度和待办事项

---

## 🚀 快速开始

### 1. 安装依赖
```bash
cd "d:\111_temu_商品\ST455\2026-project-gaogou\fair_order_dispatch"
pip install -r requirements.txt
```

### 2. 运行多种子实验（30-60分钟）
```bash
C:\Users\Administrator\AppData\Local\Programs\Python\Python39\python.exe scripts/run_multi_seed_experiments.py
```

### 3. 运行统计分析（几秒钟）
```bash
C:\Users\Administrator\AppData\Local\Programs\Python\Python39\python.exe scripts/statistical_analysis.py
```

### 4. 在 Jupyter 中查看结果
```bash
jupyter notebook final_submission_cn.ipynb
```
然后点击 "Run All"

---

## 📋 当前状态

### ✅ 已完成
- [x] 修复 notebook 中的5处编码问题
- [x] 补充参考文献到8条
- [x] 创建多种子实验脚本
- [x] 创建统计分析脚本
- [x] 创建依赖管理文件
- [x] 整理项目文件结构

### ⏳ 待完成
- [ ] 运行多种子实验
- [ ] 运行统计分析
- [ ] 更新 notebook 的结果表格和图表
- [ ] 在 Jupyter 中测试 Run All
- [ ] 添加小组贡献说明
- [ ] 最终检查和提交

---

## 💡 技术说明

- **硬件环境**: AMD 显卡，使用 CPU 版本 PyTorch
- **Python 版本**: 3.9.8
- **代码语言**: 所有代码和注释使用中文
- **实验时间**: 单次训练约1-2分钟，完整实验约30-60分钟

---

## 📞 团队协作

本项目使用团队协作模式完成：
- **doc-writer**: 补充参考文献和文档
- **notebook-fixer**: 修复编码问题
- **experiment-runner**: 编写实验脚本
- **stats-analyzer**: 编写统计分析脚本

所有修改都记录在 `docs/CHANGELOG.md` 中。

---

## 📚 更多信息

- 详细执行计划：`docs/PLAN.md`
- 修改日志：`docs/CHANGELOG.md`
- 当前进度：`docs/PROGRESS.md`
- 研究发现：`docs/findings.md`

---

**最后更新**: 2026-04-04  
**项目状态**: 准备运行实验
