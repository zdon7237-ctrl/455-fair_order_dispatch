from __future__ import annotations

import numpy as np


def _active_zones(demand_by_zone: np.ndarray) -> np.ndarray:
    active = np.flatnonzero(demand_by_zone > 0)
    return active if active.size else np.arange(demand_by_zone.size)


def _probabilities_to_logits(matrix: np.ndarray) -> np.ndarray:
    clipped = np.clip(np.asarray(matrix, dtype=np.float32), 1e-12, 1.0)
    return np.log(clipped).reshape(-1).astype(np.float32)


def local_first_policy(
    available_drivers_by_zone: np.ndarray,
    demand_by_zone: np.ndarray,
) -> np.ndarray:
    zone_count = demand_by_zone.size
    matrix = np.zeros((zone_count, zone_count), dtype=float)
    active = _active_zones(demand_by_zone)

    for zone_idx in range(zone_count):
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
    zone_count = demand_by_zone.size
    matrix = np.zeros((zone_count, zone_count), dtype=float)
    target_zone = int(np.argmax(demand_by_zone))
    matrix[:, target_zone] = 1.0
    return matrix


def flatten_policy(matrix: np.ndarray) -> np.ndarray:
    return np.asarray(matrix, dtype=np.float32).reshape(-1)


def local_first_logits(demand_by_zone: np.ndarray) -> np.ndarray:
    available = np.zeros_like(demand_by_zone, dtype=np.float32)
    return _probabilities_to_logits(
        local_first_policy(available, np.asarray(demand_by_zone))
    )


def demand_greedy_logits(demand_by_zone: np.ndarray) -> np.ndarray:
    available = np.zeros_like(demand_by_zone, dtype=np.float32)
    return _probabilities_to_logits(
        demand_greedy_policy(available, np.asarray(demand_by_zone))
    )
