from __future__ import annotations

import numpy as np
import pytest

from fair_dispatch.config import DispatchConfig
from fair_dispatch.environment import FairDispatchEnv


def _fixed_schedule(config: DispatchConfig) -> np.ndarray:
    return np.tile(np.array(config.base_lambda, dtype=int), (config.horizon, 1))


def test_reset_exposes_locked_observation_layout() -> None:
    config = DispatchConfig(horizon=3)
    env = FairDispatchEnv(config=config, scene="normal", alpha=0.2, seed=3, demand_schedule=_fixed_schedule(config))

    obs, info = env.reset(seed=5)

    assert obs.shape == (15,)
    assert obs[:6].tolist() == list(config.initial_drivers)
    assert obs[6:12].tolist() == list(config.base_lambda)
    assert obs[12] == pytest.approx(0.0)
    assert obs[13] == pytest.approx(0.0)
    assert obs[14] == pytest.approx(0.0)
    assert set(info) == {
        "fulfilled_orders",
        "completion_rate",
        "step_revenue",
        "episode_revenue",
        "current_gini",
        "bottom20_income_mean",
    }


def test_action_logits_are_reshaped_and_softmaxed_rowwise() -> None:
    env = FairDispatchEnv(config=DispatchConfig(horizon=2), alpha=0.2, demand_schedule=None)
    logits = np.arange(36, dtype=np.float32)

    probs = env.action_logits_to_matrix(logits)

    assert probs.shape == (6, 6)
    assert np.allclose(probs.sum(axis=1), 1.0)
    assert np.all(probs > 0)


def test_step_conserves_driver_count_and_uses_reward_formula() -> None:
    config = DispatchConfig(horizon=2)
    schedule = _fixed_schedule(config)
    env = FairDispatchEnv(config=config, scene="normal", alpha=0.2, seed=0, demand_schedule=schedule)
    env.reset(seed=7)

    _, reward, terminated, truncated, info = env.step(np.zeros(36, dtype=np.float32))

    assert sum(env.available_drivers_by_zone.tolist()) == config.driver_count
    assert env.cumulative_income.sum() == info["episode_revenue"]
    assert reward == pytest.approx(info["completion_rate"] - 0.2 * info["current_gini"])
    assert terminated is False
    assert truncated is False


def test_episode_terminates_at_horizon() -> None:
    config = DispatchConfig(horizon=1)
    env = FairDispatchEnv(config=config, alpha=0.2, demand_schedule=_fixed_schedule(config))
    env.reset(seed=9)

    _, _, terminated, truncated, _ = env.step(np.zeros(36, dtype=np.float32))

    assert terminated is True
    assert truncated is False
