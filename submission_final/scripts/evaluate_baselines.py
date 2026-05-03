from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from fair_dispatch.baselines import demand_greedy_logits, local_first_logits
from fair_dispatch.config import DEFAULT_CONFIG, DispatchConfig
from fair_dispatch.environment import FairDispatchEnv
from fair_dispatch.scenarios import CalibrationDecision, calibrate_shock_multiplier


RESULT_FIELDS = [
    "algorithm",
    "scene",
    "alpha",
    "episode_revenue",
    "final_episode_gini",
    "final_episode_bottom20_income_mean",
    "mean_completion_rate",
]


def rollout_baseline(
    policy_name: str,
    scene: str,
    *,
    config: DispatchConfig = DEFAULT_CONFIG,
    seed: int = 0,
    shock_multiplier: int | None = None,
) -> tuple[dict[str, float | str], list[float]]:
    # Roll one baseline episode.
    env = FairDispatchEnv(
        config=config,
        scene=scene,
        alpha=config.primary_alpha,
        shock_multiplier=shock_multiplier,
    )
    observation, info = env.reset(seed=seed)
    completion_rates: list[float] = []
    terminated = False

    while not terminated:
        # Demand sits in the middle slice.
        demand = observation[config.zone_count : config.zone_count * 2]
        if policy_name == "Local-First":
            action = local_first_logits(demand)
        elif policy_name == "Demand-Greedy":
            action = demand_greedy_logits(demand)
        else:
            raise ValueError(f"Unsupported baseline: {policy_name}")

        observation, _reward, terminated, _truncated, info = env.step(action)
        completion_rates.append(info["completion_rate"])

    row = {
        "algorithm": policy_name,
        "scene": scene,
        "alpha": "",
        "episode_revenue": info["episode_revenue"],
        "final_episode_gini": info["current_gini"],
        "final_episode_bottom20_income_mean": info["bottom20_income_mean"],
        "mean_completion_rate": float(np.mean(completion_rates)),
    }
    return row, env.cumulative_income.astype(float).tolist()


def calibrate_multiplier(
    normal_rows: list[dict[str, float | str]],
    shock_rows: list[dict[str, float | str]],
    *,
    config: DispatchConfig = DEFAULT_CONFIG,
) -> CalibrationDecision:
    # Measure the normal-vs-shock drop.
    normal_by_algorithm = {row["algorithm"]: row for row in normal_rows}
    gaps = {}
    for shock_row in shock_rows:
        algorithm = str(shock_row["algorithm"])
        normal_rate = float(normal_by_algorithm[algorithm]["mean_completion_rate"])
        shock_rate = float(shock_row["mean_completion_rate"])
        gaps[algorithm] = abs(normal_rate - shock_rate)
    return calibrate_shock_multiplier(gaps, config=config)


def write_results(rows: list[dict[str, float | str]], output_path: Path) -> None:
    # Save summary rows.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_calibration(calibration: CalibrationDecision, output_path: Path) -> None:
    # Save the frozen shock setting.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "original_multiplier": calibration.original_multiplier,
        "frozen_multiplier": calibration.frozen_multiplier,
        "threshold": calibration.threshold,
        "promoted": calibration.promoted,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_income_snapshot(
    incomes_by_algorithm: dict[str, list[float]], output_path: Path
) -> None:
    # Save shock incomes for the CDF.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["algorithm", "driver_index", "income"])
        writer.writeheader()
        for algorithm, incomes in incomes_by_algorithm.items():
            for driver_index, income in enumerate(incomes):
                writer.writerow(
                    {
                        "algorithm": algorithm,
                        "driver_index": driver_index,
                        "income": income,
                    }
                )


def main() -> None:
    default_results_dir = PROJECT_ROOT / "results"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=default_results_dir / "baseline_results.csv",
    )
    parser.add_argument(
        "--income-output",
        type=Path,
        default=default_results_dir / "baseline_shock_incomes.csv",
    )
    parser.add_argument(
        "--calibration-output",
        type=Path,
        default=default_results_dir / "shock_calibration.json",
    )
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    # Run normal first.
    normal_results = [
        rollout_baseline("Local-First", "normal", seed=args.seed),
        rollout_baseline("Demand-Greedy", "normal", seed=args.seed),
    ]
    shock_results = [
        rollout_baseline("Local-First", "shock", seed=args.seed),
        rollout_baseline("Demand-Greedy", "shock", seed=args.seed),
    ]
    normal_rows = [row for row, _incomes in normal_results]
    shock_rows = [row for row, _incomes in shock_results]

    calibration = calibrate_multiplier(normal_rows, shock_rows)
    if calibration.promoted:
        # Re-run shock with the promoted multiplier.
        shock_results = [
            rollout_baseline(
                "Local-First",
                "shock",
                seed=args.seed,
                shock_multiplier=calibration.frozen_multiplier,
            ),
            rollout_baseline(
                "Demand-Greedy",
                "shock",
                seed=args.seed,
                shock_multiplier=calibration.frozen_multiplier,
            ),
        ]
        shock_rows = [row for row, _incomes in shock_results]

    write_results(normal_rows + shock_rows, args.output)
    write_calibration(calibration, args.calibration_output)
    write_income_snapshot(
        {row["algorithm"]: incomes for row, incomes in shock_results},
        args.income_output,
    )
    print(
        f"Wrote {len(normal_rows) + len(shock_rows)} baseline rows "
        f"with shock multiplier {calibration.frozen_multiplier}."
    )


if __name__ == "__main__":
    main()
