<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/__init__.py
=======
"""Public imports for the fair dispatch package."""

>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/__init__.py
from fair_dispatch.baselines import (
    demand_greedy_logits,
    demand_greedy_policy,
    local_first_logits,
    local_first_policy,
)
from fair_dispatch.config import DEFAULT_CONFIG, DispatchConfig
from fair_dispatch.environment import FairDispatchEnv
from fair_dispatch.metrics import bottom_percent_mean, bottom20_income_mean, gini_coefficient

<<<<<<< Updated upstream:fair_order_dispatch-作业版本/src/fair_dispatch/__init__.py
=======
# Re-export the main API.
>>>>>>> Stashed changes:submission_ready/src/fair_dispatch/__init__.py
__all__ = [
    "DEFAULT_CONFIG",
    "DispatchConfig",
    "FairDispatchEnv",
    "bottom_percent_mean",
    "bottom20_income_mean",
    "demand_greedy_logits",
    "demand_greedy_policy",
    "gini_coefficient",
    "local_first_logits",
    "local_first_policy",
]
