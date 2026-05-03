import importlib.util
from pathlib import Path

import numpy as np


def _load_train_ppo_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "train_ppo.py"
    spec = importlib.util.spec_from_file_location("train_ppo", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


train_ppo = _load_train_ppo_module()


class _FakePPO:
    def __init__(self, _policy, env, verbose, seed):
        self.env = env
        self.verbose = verbose
        self.seed = seed

    def learn(self, total_timesteps, callback=None):
        self.total_timesteps = total_timesteps
        self.callback = callback
        return self

    def predict(self, observation, deterministic=True):
        return np.zeros(self.env.action_space.shape, dtype=np.float32), None


def test_load_shock_multiplier_uses_default_when_file_is_missing(tmp_path):
    missing = tmp_path / "missing.json"

    assert train_ppo.load_shock_multiplier(missing) == train_ppo.DEFAULT_CONFIG.shock_multiplier


def test_train_and_evaluate_ppo_returns_expected_schema(monkeypatch):
    monkeypatch.setattr(train_ppo, "_load_ppo", lambda: _FakePPO)

    row, incomes = train_ppo.train_and_evaluate_ppo(
        alpha=0.2,
        scene="normal",
        total_timesteps=8,
        seed=5,
        shock_multiplier=train_ppo.DEFAULT_CONFIG.shock_multiplier,
    )

    assert row["algorithm"] == "PPO"
    assert row["scene"] == "normal"
    assert row["alpha"] == 0.2
    assert len(incomes) == train_ppo.DEFAULT_CONFIG.driver_count
    assert set(row) == {
        "algorithm",
        "scene",
        "alpha",
        "episode_revenue",
        "final_episode_gini",
        "final_episode_bottom20_income_mean",
        "mean_completion_rate",
    }
