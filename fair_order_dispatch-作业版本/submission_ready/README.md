# Fair Order Dispatch

## 权威提交文件

- `final_submission_cn.ipynb`
- `final_submission_en.ipynb`

这两个 notebook 是当前项目的正式报告版本，内容应保持一致，仅语言不同。

`notebooks/fair_order_dispatch_report.ipynb` 是历史草稿，用于开发过程中的整理与存档，不作为最终提交材料。

## 项目概览

本项目研究需求冲击下订单派单的效率与公平权衡。我们构建了一个区域级仿真环境，在合成需求数据上比较三类策略：

- `Local-First`：更强、也更现实的规则基线
- `Demand-Greedy`：sanity-check baseline，用于展示极端追逐热点区域的后果
- `PPO`：在 fairness-aware reward 下学习得到的区域级派单策略

核心指标包括：

- `episode_revenue`
- `final_episode_gini`
- `bottom20_income_mean`

## 仓库结构

```text
fair_order_dispatch-作业版本/
├── final_submission_cn.ipynb
├── final_submission_en.ipynb
├── README.md
├── requirements.txt
├── pyproject.toml
├── docs/
│   ├── COLAB使用指南.md
│   ├── PLAN.md
│   ├── PROGRESS.md
│   ├── CHANGELOG.md
│   └── findings.md
├── src/fair_dispatch/
│   ├── __init__.py
│   ├── config.py
│   ├── environment.py
│   ├── metrics.py
│   ├── baselines.py
│   └── scenarios.py
├── scripts/
│   ├── evaluate_baselines.py
│   ├── train_ppo.py
│   ├── run_multi_seed_experiments.py
│   ├── statistical_analysis.py
│   └── plot_results.py
├── results/
├── figures/
├── colab_upload/
└── notebooks/
    └── fair_order_dispatch_report.ipynb
```

## 结果与复现

当前仓库已经包含保存好的实验结果：

- `results/multi_seed_results.csv`
- `results/statistical_summary.csv`
- `results/significance_tests.csv`
- `figures/*.png`

正式 notebook 默认读取这些文件并重建表格与图形，不会在打开时重新训练模型。

如果需要从头复现结果，可以：

1. 本地安装依赖：

```bash
pip install -r requirements.txt
```

2. 重新运行多种子实验：

```bash
python scripts/run_multi_seed_experiments.py
```

3. 重新运行统计分析与图表生成：

```bash
python scripts/statistical_analysis.py
```

如果更适合在云端运行，推荐直接参考 `docs/COLAB使用指南.md` 在 Google Colab 中完成批量实验。

## 使用建议

- 如果只查看最终报告，优先打开 `final_submission_cn.ipynb` 或 `final_submission_en.ipynb`。
- 如果需要阅读源码实现，查看 `src/fair_dispatch/`。
- 如果需要重跑实验流程，查看 `scripts/` 和 `docs/COLAB使用指南.md`。
