# Submission Notes

This folder is the cleaned submission bundle.

Included:

- `final_submission_cn.ipynb`
- `final_submission_en.ipynb`
- `README.md`
- `requirements.txt`
- `pyproject.toml`
- `src/`
- `scripts/`
- `results/`
- `figures/`
- `tests/`
- `docs/COLAB使用指南.md`

If you want to rerun the experiments and refresh the saved results/figures before submission, run the commands from inside this folder:

```bash
python scripts/evaluate_baselines.py
python scripts/train_ppo.py --seed 0 --total-timesteps 20000
python scripts/run_multi_seed_experiments.py --total-timesteps 20000
python scripts/statistical_analysis.py
```

That will regenerate the CSV files under `results/`, including the shock income snapshots used by the CDF plot, and the figures under `figures/`, so the submission bundle stays self-contained.
