"""Shared settings for the small dispatch simulator."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DispatchConfig:
    """Keep the experiment numbers in one place so scripts do not drift."""

    zone_count: int = 6
    driver_count: int = 60
    horizon: int = 40
    base_lambda: tuple[int, ...] = (4, 6, 5, 7, 4, 5)
    initial_drivers: tuple[int, ...] = (8, 12, 10, 13, 8, 9)
    shock_zone: int = 3
    shock_start: int = 15
    shock_end: int = 24
    shock_multiplier: int = 3
    promoted_shock_multiplier: int = 5
    alpha_grid: tuple[float, ...] = (0.0, 0.1, 0.2, 0.4)
    primary_alpha: float = 0.2

    def __post_init__(self) -> None:
        # Keep vector sizes aligned.
        if self.zone_count != len(self.base_lambda):
            raise ValueError("zone_count must match base_lambda length")
        if self.zone_count != len(self.initial_drivers):
            raise ValueError("zone_count must match initial_drivers length")
        if self.driver_count != sum(self.initial_drivers):
            raise ValueError("driver_count must equal the initial driver total")
        if self.horizon < 1:
            raise ValueError("horizon must be positive")
        if not 0 <= self.shock_zone < self.zone_count:
            raise ValueError("shock_zone must be within the configured zones")
        # Keep the shock window in range.
        clamped_start = min(self.shock_start, self.horizon - 1)
        clamped_end = min(max(clamped_start, self.shock_end), self.horizon - 1)
        object.__setattr__(self, "shock_start", clamped_start)
        object.__setattr__(self, "shock_end", clamped_end)
        if self.shock_multiplier < 1 or self.promoted_shock_multiplier < 1:
            raise ValueError("shock multipliers must be positive")


DEFAULT_CONFIG = DispatchConfig()
