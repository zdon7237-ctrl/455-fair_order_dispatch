<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/scenarios.py
=======
"""Demand generators for the normal and shock scenes."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/scenarios.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np

from fair_dispatch.config import DEFAULT_CONFIG, DispatchConfig


@dataclass(frozen=True)
class CalibrationDecision:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/scenarios.py
=======
    """Record which shock multiplier we froze before running PPO."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/scenarios.py
    original_multiplier: int
    frozen_multiplier: int
    threshold: float
    promoted: bool


def build_normal_demand_schedule(
    config: DispatchConfig = DEFAULT_CONFIG,
    *,
    seed: int | None = None,
) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/scenarios.py
=======
    """Draw one normal episode from Poisson demand."""

    # Sample one full episode.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/scenarios.py
    rng = np.random.default_rng(seed)
    return rng.poisson(
        lam=np.asarray(config.base_lambda, dtype=float),
        size=(config.horizon, config.zone_count),
    ).astype(np.int32)


def build_shock_demand_schedule(
    config: DispatchConfig = DEFAULT_CONFIG,
    *,
    seed: int | None = None,
    shock_multiplier: int | None = None,
) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/scenarios.py
    demands = build_normal_demand_schedule(config, seed=seed)
    multiplier = shock_multiplier or config.shock_multiplier
=======
    """Start with normal demand, then multiply one zone during the shock window."""

    demands = build_normal_demand_schedule(config, seed=seed)
    multiplier = shock_multiplier or config.shock_multiplier
    # Boost one zone inside the window.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/scenarios.py
    demands[config.shock_start : config.shock_end + 1, config.shock_zone] *= multiplier
    return demands


def sample_episode_demands(
    config: DispatchConfig = DEFAULT_CONFIG,
    *,
    scene: str = "normal",
    seed: int | None = None,
    shock_multiplier: int | None = None,
) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/scenarios.py
=======
    """Pick the right demand generator for the requested scene."""

    # Switch by scene.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/scenarios.py
    if scene == "normal":
        return build_normal_demand_schedule(config, seed=seed)
    if scene == "shock":
        return build_shock_demand_schedule(
            config,
            seed=seed,
            shock_multiplier=shock_multiplier,
        )
    raise ValueError(f"Unsupported scene: {scene}")


def shock_flag_for_step(
    step_index: int,
    *,
    config: DispatchConfig = DEFAULT_CONFIG,
    scene: str = "normal",
) -> float:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/scenarios.py
=======
    """Expose the shock window as a 0/1 feature in the observation."""

    # Mark the shock window.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/scenarios.py
    if scene != "shock":
        return 0.0
    return float(config.shock_start <= step_index <= config.shock_end)


def calibrate_shock_multiplier(
    baseline_completion_rates: Mapping[str, float | Mapping[str, float]],
    *,
    config: DispatchConfig = DEFAULT_CONFIG,
    current_multiplier: int | None = None,
    promoted_multiplier: int | None = None,
    threshold: float = 0.05,
) -> CalibrationDecision:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/scenarios.py
=======
    """Use the stronger shock only when the default shock is too mild."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/scenarios.py
    original = config.shock_multiplier if current_multiplier is None else current_multiplier
    promoted = (
        config.promoted_shock_multiplier
        if promoted_multiplier is None
        else promoted_multiplier
    )
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/scenarios.py
=======
    # Compare the normal-vs-shock gap.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/scenarios.py
    gaps: list[float] = []
    for values in baseline_completion_rates.values():
        if isinstance(values, Mapping):
            gaps.append(float(values["normal"]) - float(values["shock"]))
        else:
            gaps.append(float(values))

<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/scenarios.py
=======
    # Promote only if every gap stays small.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/scenarios.py
    should_promote = all(gap < threshold for gap in gaps)
    return CalibrationDecision(
        original_multiplier=original,
        frozen_multiplier=promoted if should_promote else original,
        threshold=threshold,
        promoted=should_promote,
    )
