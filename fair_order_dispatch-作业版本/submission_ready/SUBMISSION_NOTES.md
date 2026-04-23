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
python scripts/run_multi_seed_experiments.py
python scripts/statistical_analysis.py
```

That will regenerate the CSV files under `results/` and the figures under `figures/`, so the submission bundle stays self-contained.
