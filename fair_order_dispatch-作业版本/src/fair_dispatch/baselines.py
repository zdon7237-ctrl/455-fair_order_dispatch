<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/baselines.py
=======
"""Simple rule policies used as baselines for PPO."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/baselines.py
from __future__ import annotations

import numpy as np


def _active_zones(demand_by_zone: np.ndarray) -> np.ndarray:
    active = np.flatnonzero(demand_by_zone > 0)
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/baselines.py
=======
    # Fall back to all zones.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/baselines.py
    return active if active.size else np.arange(demand_by_zone.size)


def _probabilities_to_logits(matrix: np.ndarray) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/baselines.py
=======
    # Match the env action shape.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/baselines.py
    clipped = np.clip(np.asarray(matrix, dtype=np.float32), 1e-12, 1.0)
    return np.log(clipped).reshape(-1).astype(np.float32)


def local_first_policy(
    available_drivers_by_zone: np.ndarray,
    demand_by_zone: np.ndarray,
) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/baselines.py
=======
    """Stay local if there is demand; otherwise spread to zones with orders."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/baselines.py
    zone_count = demand_by_zone.size
    matrix = np.zeros((zone_count, zone_count), dtype=float)
    active = _active_zones(demand_by_zone)

    for zone_idx in range(zone_count):
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/baselines.py
=======
        # Stay local when demand exists.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/baselines.py
        if demand_by_zone[zone_idx] > 0:
            matrix[zone_idx, zone_idx] = 1.0
        else:
            share = 1.0 / active.size
            matrix[zone_idx, active] = share

    return matrix


def demand_greedy_policy(
    available_drivers_by_zone: np.ndarray,
    demand_by_zone: np.ndarray,
) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/baselines.py
    zone_count = demand_by_zone.size
    matrix = np.zeros((zone_count, zone_count), dtype=float)
=======
    """Send every available driver to the zone with the most current demand."""

    zone_count = demand_by_zone.size
    matrix = np.zeros((zone_count, zone_count), dtype=float)
    # Send everyone to the busiest zone.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/baselines.py
    target_zone = int(np.argmax(demand_by_zone))
    matrix[:, target_zone] = 1.0
    return matrix


def flatten_policy(matrix: np.ndarray) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/baselines.py
=======
    """Flatten a zone-to-zone matrix into the action format used by the env."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/baselines.py
    return np.asarray(matrix, dtype=np.float32).reshape(-1)


def local_first_logits(demand_by_zone: np.ndarray) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/baselines.py
=======
    """Return Local-First as logits, because the environment expects logits."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/baselines.py
    available = np.zeros_like(demand_by_zone, dtype=np.float32)
    return _probabilities_to_logits(
        local_first_policy(available, np.asarray(demand_by_zone))
    )


def demand_greedy_logits(demand_by_zone: np.ndarray) -> np.ndarray:
<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/baselines.py
=======
    """Return Demand-Greedy as logits for the same action interface."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/baselines.py
    available = np.zeros_like(demand_by_zone, dtype=np.float32)
    return _probabilities_to_logits(
        demand_greedy_policy(available, np.asarray(demand_by_zone))
    )
