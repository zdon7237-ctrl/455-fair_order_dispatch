import numpy as np

from fair_dispatch.config import DEFAULT_CONFIG
from fair_dispatch.scenarios import (
    calibrate_shock_multiplier,
    sample_episode_demands,
    shock_flag_for_step,
)


def test_default_config_driver_total_matches_initial_distribution():
    assert sum(DEFAULT_CONFIG.initial_drivers) == DEFAULT_CONFIG.driver_count


def test_normal_demand_sampling_is_reproducible_for_same_seed():
    first = sample_episode_demands(DEFAULT_CONFIG, scene="normal", seed=11)
    second = sample_episode_demands(DEFAULT_CONFIG, scene="normal", seed=11)

    assert np.array_equal(first, second)


def test_shock_sampling_only_scales_target_zone_inside_window():
    normal = sample_episode_demands(DEFAULT_CONFIG, scene="normal", seed=17)
    shock = sample_episode_demands(DEFAULT_CONFIG, scene="shock", seed=17)

    assert np.array_equal(
        normal[: DEFAULT_CONFIG.shock_start, DEFAULT_CONFIG.shock_zone],
        shock[: DEFAULT_CONFIG.shock_start, DEFAULT_CONFIG.shock_zone],
    )
    assert np.array_equal(
        normal[DEFAULT_CONFIG.shock_end + 1 :, DEFAULT_CONFIG.shock_zone],
        shock[DEFAULT_CONFIG.shock_end + 1 :, DEFAULT_CONFIG.shock_zone],
    )
    assert np.array_equal(
        normal[:, : DEFAULT_CONFIG.shock_zone],
        shock[:, : DEFAULT_CONFIG.shock_zone],
    )
    assert np.array_equal(
        normal[:, DEFAULT_CONFIG.shock_zone + 1 :],
        shock[:, DEFAULT_CONFIG.shock_zone + 1 :],
    )
    assert np.array_equal(
        shock[
            DEFAULT_CONFIG.shock_start : DEFAULT_CONFIG.shock_end + 1,
            DEFAULT_CONFIG.shock_zone,
        ],
        normal[
            DEFAULT_CONFIG.shock_start : DEFAULT_CONFIG.shock_end + 1,
            DEFAULT_CONFIG.shock_zone,
        ]
        * DEFAULT_CONFIG.shock_multiplier,
    )


def test_shock_flag_tracks_window_for_shock_scene():
    assert shock_flag_for_step(DEFAULT_CONFIG.shock_start - 1, scene="shock") == 0.0
    assert shock_flag_for_step(DEFAULT_CONFIG.shock_start, scene="shock") == 1.0
    assert shock_flag_for_step(DEFAULT_CONFIG.shock_end, scene="shock") == 1.0
    assert shock_flag_for_step(DEFAULT_CONFIG.shock_end + 1, scene="shock") == 0.0


def test_calibration_promotes_multiplier_when_all_gaps_are_small():
    decision = calibrate_shock_multiplier(
        {"Local-First": 0.01, "Demand-Greedy": 0.03},
        config=DEFAULT_CONFIG,
    )

    assert decision.promoted is True
    assert decision.frozen_multiplier == DEFAULT_CONFIG.promoted_shock_multiplier

