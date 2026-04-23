from __future__ import annotations

import pytest

from fair_dispatch.metrics import bottom_percent_mean, gini_coefficient


def test_gini_is_zero_for_empty_or_equal_income() -> None:
    assert gini_coefficient([]) == pytest.approx(0.0)
    assert gini_coefficient([0, 0, 0]) == pytest.approx(0.0)
    assert gini_coefficient([3, 3, 3]) == pytest.approx(0.0)


def test_gini_matches_known_imbalanced_case() -> None:
    assert gini_coefficient([0, 0, 0, 10]) == pytest.approx(0.75)


def test_bottom_percent_mean_uses_lowest_income_tail() -> None:
    incomes = [1, 2, 3, 100, 200]

    assert bottom_percent_mean(incomes, share=0.2) == pytest.approx(1.0)
    assert bottom_percent_mean(incomes, share=0.4) == pytest.approx(1.5)


def test_bottom_percent_mean_handles_empty_income() -> None:
    assert bottom_percent_mean([], share=0.2) == pytest.approx(0.0)
