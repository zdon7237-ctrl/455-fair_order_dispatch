from __future__ import annotations

import numpy as np
import pytest

from fair_dispatch.baselines import demand_greedy_logits, local_first_logits


def _softmax_rows(flat_logits: np.ndarray, zone_count: int = 6) -> np.ndarray:
    matrix = flat_logits.reshape(zone_count, zone_count)
    shifted = matrix - matrix.max(axis=1, keepdims=True)
    exp = np.exp(shifted)
    return exp / exp.sum(axis=1, keepdims=True)


def test_local_first_prefers_local_zone_with_demand_and_spreads_otherwise() -> None:
    demand = np.array([1, 0, 2, 0, 0, 0], dtype=int)

    logits = local_first_logits(demand)
    probs = _softmax_rows(logits)

    assert logits.shape == (36,)
    assert probs[0, 0] > 0.99
    assert probs[2, 2] > 0.99
    assert probs[1, 0] == pytest.approx(0.5, abs=1e-3)
    assert probs[1, 2] == pytest.approx(0.5, abs=1e-3)
    assert np.all(probs[1, [1, 3, 4, 5]] < 1e-6)


def test_demand_greedy_routes_every_zone_to_max_demand_destination() -> None:
    demand = np.array([2, 4, 1, 9, 3, 2], dtype=int)

    logits = demand_greedy_logits(demand)
    probs = _softmax_rows(logits)

    assert logits.shape == (36,)
    assert np.all(probs[:, 3] > 0.99)
    assert np.all(probs[:, np.arange(6) != 3] < 1e-6)
