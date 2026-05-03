"""Fairness metrics for driver income at the end of an episode."""

from __future__ import annotations

import math

import numpy as np


def gini_coefficient(values: np.ndarray) -> float:
    """Return 0 for equal incomes and closer to 1 when income is more uneven."""

    # Work on sorted incomes.
    ordered = np.sort(np.asarray(values, dtype=float))
    if ordered.size == 0:
        return 0.0
    total = ordered.sum()
    if total <= 0.0:
        return 0.0

    count = ordered.size
    weighted_sum = np.dot(np.arange(1, count + 1, dtype=float), ordered)
    gini = (2.0 * weighted_sum) / (count * total) - (count + 1) / count
    return float(max(0.0, min(1.0, gini)))


def bottom_percent_mean(values: np.ndarray, *, share: float = 0.2) -> float:
    """Average the lower-income slice of drivers."""

    # Slice the lower tail.
    incomes = np.sort(np.asarray(values, dtype=float))
    if incomes.size == 0:
        return 0.0
    if not 0.0 < share <= 1.0:
        raise ValueError("share must be in (0, 1]")
    cutoff = max(1, math.ceil(incomes.size * share))
    return float(np.mean(incomes[:cutoff]))


def bottom20_income_mean(values: np.ndarray) -> float:
    """Small helper for the bottom 20% metric used in the report."""

    return bottom_percent_mean(values, share=0.2)
