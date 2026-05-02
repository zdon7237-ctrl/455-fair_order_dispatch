<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
"""Gym-style dispatch environment used by the PPO experiments."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from fair_dispatch.config import DEFAULT_CONFIG, DispatchConfig
from fair_dispatch.metrics import bottom20_income_mean, gini_coefficient
from fair_dispatch.scenarios import sample_episode_demands, shock_flag_for_step

try:
    import gymnasium as gym
    from gymnasium import spaces
except ImportError:  # pragma: no cover
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
    # Keep tests running without gymnasium.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
    class _FallbackEnv:
        pass

    @dataclass
    class _FallbackBox:
        low: Any
        high: Any
        shape: tuple[int, ...]
        dtype: Any

    class _FallbackSpaces:
        Box = _FallbackBox

    class _FallbackGym:
        Env = _FallbackEnv

    gym = _FallbackGym()
    spaces = _FallbackSpaces()


class FairDispatchEnv(gym.Env):
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
    """A small zone-level simulator with driver movement, demand, and income."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
    metadata = {"render_modes": []}

    def __init__(
        self,
        *,
        config: DispatchConfig = DEFAULT_CONFIG,
        scene: str = "normal",
        alpha: float | None = None,
        shock_multiplier: int | None = None,
        seed: int | None = None,
        demand_schedule: np.ndarray | None = None,
    ) -> None:
        self.config = config
        self.scene = scene
        self.alpha = config.primary_alpha if alpha is None else alpha
        self.shock_multiplier = shock_multiplier or config.shock_multiplier
        self.seed = seed
        self._provided_demand_schedule = None if demand_schedule is None else np.asarray(
            demand_schedule, dtype=np.int32
        )
        self.observation_space = spaces.Box(
            low=0.0,
            high=np.inf,
            shape=(15,),
            dtype=np.float32,
        )
        self.action_space = spaces.Box(
            low=-5.0,
            high=5.0,
            shape=(config.zone_count * config.zone_count,),
            dtype=np.float32,
        )

        self.rng = np.random.default_rng()
        self.episode_demands = np.zeros((config.horizon, config.zone_count), dtype=np.int32)
        self.driver_zones = np.zeros(config.driver_count, dtype=np.int32)
        self.cumulative_income = np.zeros(config.driver_count, dtype=np.float32)
        self.current_step = 0
        self.episode_revenue = 0.0
        self.previous_gini = 0.0
        self.last_allocation_matrix = np.eye(config.zone_count, dtype=np.float32)

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, float]]:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
        """Start a fresh episode and return the first observation."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        elif self.seed is not None:
            self.rng = np.random.default_rng(self.seed)

<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
        # Reset episode state.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
        self.current_step = 0
        self.episode_revenue = 0.0
        self.previous_gini = 0.0
        self.last_allocation_matrix = np.eye(self.config.zone_count, dtype=np.float32)
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
        # Rebuild the starting zone split.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
        self.driver_zones = np.concatenate(
            [
                np.full(count, zone_idx, dtype=np.int32)
                for zone_idx, count in enumerate(self.config.initial_drivers)
            ]
        )
        self.cumulative_income = np.zeros(self.config.driver_count, dtype=np.float32)
        if self._provided_demand_schedule is not None:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
            # Reuse a fixed test schedule.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
            self.episode_demands = self._provided_demand_schedule.copy()
        else:
            self.episode_demands = sample_episode_demands(
                self.config,
                scene=self.scene,
                seed=self.seed if seed is None else seed,
                shock_multiplier=self.shock_multiplier,
            )

        info = self._info(fulfilled_orders=0, completion_rate=0.0, step_revenue=0.0)
        return self._observation(), info

    def step(
        self, action: np.ndarray
    ) -> tuple[np.ndarray, float, bool, bool, dict[str, float]]:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
        """Move drivers according to the action, match orders, and score the step."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
        if self.current_step >= self.config.horizon:
            raise RuntimeError("Episode has already terminated. Call reset().")

        demand = self.episode_demands[self.current_step].copy()
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
        # Turn logits into row-wise probabilities.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
        allocation = self.action_logits_to_matrix(action)
        self.last_allocation_matrix = allocation

        assignments: dict[int, list[tuple[int, int]]] = {
            zone_idx: [] for zone_idx in range(self.config.zone_count)
        }
        source_zones = self.driver_zones.copy()

        for zone_idx in range(self.config.zone_count):
            driver_indices = np.flatnonzero(source_zones == zone_idx)
            if driver_indices.size == 0:
                continue
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
            # Sample where each driver tries to go.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
            destinations = self.rng.choice(
                self.config.zone_count,
                size=driver_indices.size,
                p=allocation[zone_idx],
            )
            for driver_index, destination in zip(driver_indices, destinations):
                assignments[int(destination)].append((int(driver_index), zone_idx))

        fulfilled_orders = 0
        updated_zones = source_zones.copy()

        for destination_zone, assigned_drivers in assignments.items():
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
            # Matches cannot exceed local demand.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
            max_matches = min(len(assigned_drivers), int(demand[destination_zone]))
            if max_matches == 0:
                continue
            chosen = self.rng.choice(len(assigned_drivers), size=max_matches, replace=False)
            for local_idx in np.asarray(chosen, dtype=int):
                driver_index, _source_zone = assigned_drivers[local_idx]
                updated_zones[driver_index] = destination_zone
                self.cumulative_income[driver_index] += 1.0
                fulfilled_orders += 1

        self.driver_zones = updated_zones
        self.episode_revenue += float(fulfilled_orders)
        current_gini = gini_coefficient(self.cumulative_income)
        completion_rate = fulfilled_orders / max(1, int(demand.sum()))
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
        # Trade off fill rate and fairness.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
        reward = float(completion_rate - self.alpha * current_gini)
        self.previous_gini = current_gini

        self.current_step += 1
        terminated = self.current_step >= self.config.horizon
        info = self._info(
            fulfilled_orders=fulfilled_orders,
            completion_rate=float(completion_rate),
            step_revenue=float(fulfilled_orders),
        )
        return self._observation(), reward, terminated, False, info

    def action_logits_to_matrix(self, action: np.ndarray) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
        logits = np.asarray(action, dtype=np.float32).reshape(
            self.config.zone_count, self.config.zone_count
        )
=======
        """Convert the flat action vector into zone-to-zone probabilities."""

        logits = np.asarray(action, dtype=np.float32).reshape(
            self.config.zone_count, self.config.zone_count
        )
        # Softmax each source row.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
        logits = logits - logits.max(axis=1, keepdims=True)
        weights = np.exp(logits)
        return weights / weights.sum(axis=1, keepdims=True)

    @property
    def available_drivers_by_zone(self) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
        """Count how many drivers are currently in each zone."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
        return np.bincount(
            self.driver_zones, minlength=self.config.zone_count
        ).astype(np.float32)

    def _current_demand(self) -> np.ndarray:
        if self.current_step >= self.config.horizon:
            return np.zeros(self.config.zone_count, dtype=np.float32)
        return self.episode_demands[self.current_step].astype(np.float32)

    def _observation(self) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/environment.py
=======
        """Build the 15-number state vector used by PPO."""

        # Pack drivers, demand, and context.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/environment.py
        return np.concatenate(
            [
                self.available_drivers_by_zone,
                self._current_demand(),
                np.array(
                    [
                        self.current_step / self.config.horizon,
                        self.previous_gini,
                        shock_flag_for_step(
                            self.current_step, config=self.config, scene=self.scene
                        ),
                    ],
                    dtype=np.float32,
                ),
            ]
        ).astype(np.float32)

    def _info(
        self,
        *,
        fulfilled_orders: int,
        completion_rate: float,
        step_revenue: float,
    ) -> dict[str, float]:
        return {
            "fulfilled_orders": float(fulfilled_orders),
            "completion_rate": float(completion_rate),
            "step_revenue": float(step_revenue),
            "episode_revenue": float(self.episode_revenue),
            "current_gini": float(gini_coefficient(self.cumulative_income)),
            "bottom20_income_mean": float(bottom20_income_mean(self.cumulative_income)),
        }
