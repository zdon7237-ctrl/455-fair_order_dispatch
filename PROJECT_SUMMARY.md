# Project Summary: Fair Order Dispatch Under Demand Shock

This project studies a small ride-hailing style order dispatch problem with a focus on the trade-off between platform efficiency and driver-income fairness. The simulator has 6 zones, 60 drivers, and 40 decision steps per episode. Demand is synthetically generated, with a calibrated shock in one zone during the middle of the episode.

The main comparison is between:

- `Local-First`: drivers first serve demand in their current zone.
- `Demand-Greedy`: drivers are sent to the current highest-demand zone.
- `PPO`: a Gym-style reinforcement learning policy trained with reward `completion_rate - alpha * gini`.

The PPO training and 10-seed batch experiments were run in Google Colab. The final English report notebook reads the saved experiment outputs in `results/` and regenerates the figures in `figures/`, so markers can inspect the report without retraining PPO. The main reported setting is `PPO(alpha=0.2)`.

## Main Result

In the shock scene, `PPO(alpha=0.2)` lowers final driver-income Gini relative to `Local-First`:

- PPO shock revenue: `1252.2 +/- 30.9`
- Local-First shock revenue: `1289.9 +/- 31.2`
- Paired revenue difference (PPO - Local-First): `-37.7`, 95% CI `[-55.5, -19.9]`, `p = 0.0010`
- PPO shock Gini: `0.0835 +/- 0.0109`
- Local-First shock Gini: `0.1104 +/- 0.0165`
- Paired Gini difference (PPO - Local-First): `-0.0268`, 95% CI `[-0.0391, -0.0145]`, `p = 0.0008`

The cautious conclusion is that PPO improves fairness in this simulator, but the paired 10-seed comparison also shows a statistically clear revenue cost relative to `Local-First`. The result is best read as an efficiency-fairness trade-off rather than an unqualified improvement.

## Folder Contents

- `README.md`: original ST455 assignment brief.
- `PROJECT_SUMMARY.md`: this project-specific overview.
- `final_submission_en.ipynb`: English final report.
- `final_submission_cn.ipynb`: Chinese version retained for reference; the English notebook is the intended submission report.
- `src/fair_dispatch/`: simulator, demand scenarios, metrics, and baseline policies.
- `scripts/`: scripts for baseline evaluation, PPO training, multi-seed experiments, statistics, and plotting.
- `results/`: saved CSV and JSON outputs used by the report.
- `figures/`: saved report figures.
- `requirements.txt`: dependency list.
- `pyproject.toml`: package metadata and core dependencies.

## Reproducing The Saved Results

The notebooks are designed to load the saved CSV files by default, so they can be reviewed without retraining PPO. To rerun the full workflow from this folder:

```bash
pip install -q -r requirements.txt
python scripts/evaluate_baselines.py
python scripts/train_ppo.py --seed 0 --total-timesteps 20000
python scripts/run_multi_seed_experiments.py --seeds 0,42,123,456,789,2025,2026,2027,2028,2029 --total-timesteps 20000
python scripts/statistical_analysis.py --alpha 0.2
```

The full multi-seed PPO run can take a long time on Colab CPU. A GPU runtime is recommended. If only refreshing tables and figures from the saved results, run:

```bash
python scripts/statistical_analysis.py --alpha 0.2
```

## Notes For Marking

The project uses synthetic data rather than real platform data. This keeps the experiment reproducible and allows direct comparison across seeds, but it also means the results should be interpreted as simulator evidence rather than production deployment evidence.

The fairness reward uses the full cumulative driver-income vector internally, while the PPO policy observes only aggregate zone state and previous Gini. The report states this limitation explicitly.

The significance tests use paired comparisons on per-seed differences because each policy is evaluated on the same seed set. With only 10 seeds, the confidence intervals and p-values should still be read as limited simulator evidence rather than definitive platform-level evidence.
