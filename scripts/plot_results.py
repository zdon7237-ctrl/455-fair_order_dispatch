"""Small plotting helper for the saved CSV results."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from fair_dispatch.config import DEFAULT_CONFIG


def read_rows(path: Path) -> list[dict[str, str]]:
    # Missing files mean no rows.
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _float(row: dict[str, str], key: str) -> float:
    value = row[key]
    return float(value) if value != "" else 0.0


def _primary_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    # Keep the main PPO setting.
    primary = []
    for row in rows:
        if row["algorithm"] != "PPO":
            primary.append(row)
        elif row["alpha"] in {"0.2", "0.20000000000000001"}:
            primary.append(row)
    return primary


def plot_revenue_by_scene(rows: list[dict[str, str]], output_dir: Path) -> None:
    """Compare total completed orders in normal and shock scenes."""

    output_dir.mkdir(parents=True, exist_ok=True)
    filtered = _primary_rows(rows)
    # Keep one algorithm order.
    algorithms = [row["algorithm"] for row in filtered if row["scene"] == "normal"]
    normal = [_float(row, "episode_revenue") for row in filtered if row["scene"] == "normal"]
    shock = [_float(row, "episode_revenue") for row in filtered if row["scene"] == "shock"]
    positions = range(len(algorithms))

    plt.figure(figsize=(8, 4))
    plt.bar([p - 0.2 for p in positions], normal, width=0.4, label="normal")
    plt.bar([p + 0.2 for p in positions], shock, width=0.4, label="shock")
    plt.xticks(list(positions), algorithms)
    plt.ylabel("Episode revenue")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "episode_revenue_by_scene.png")
    plt.close()


def plot_gini_by_scene(rows: list[dict[str, str]], output_dir: Path) -> None:
    """Compare final driver-income Gini in normal and shock scenes."""

    filtered = _primary_rows(rows)
    # Reuse the revenue order.
    algorithms = [row["algorithm"] for row in filtered if row["scene"] == "normal"]
    normal = [_float(row, "final_episode_gini") for row in filtered if row["scene"] == "normal"]
    shock = [_float(row, "final_episode_gini") for row in filtered if row["scene"] == "shock"]
    positions = range(len(algorithms))

    plt.figure(figsize=(8, 4))
    plt.bar([p - 0.2 for p in positions], normal, width=0.4, label="normal")
    plt.bar([p + 0.2 for p in positions], shock, width=0.4, label="shock")
    plt.xticks(list(positions), algorithms)
    plt.ylabel("Final episode Gini")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "final_gini_by_scene.png")
    plt.close()


def plot_alpha_tradeoff(rows: list[dict[str, str]], output_dir: Path) -> None:
    """Plot the PPO revenue/fairness trade-off for the shock scene."""

    # Plot only PPO shock runs.
    ppo_rows = [row for row in rows if row["algorithm"] == "PPO" and row["scene"] == "shock"]
    plt.figure(figsize=(6, 4))
    for row in ppo_rows:
        plt.scatter(
            _float(row, "final_episode_gini"),
            _float(row, "episode_revenue"),
            label=f"alpha={row['alpha']}",
        )
    plt.xlabel("Final episode Gini")
    plt.ylabel("Episode revenue")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "alpha_tradeoff.png")
    plt.close()


def plot_income_cdf(rows: list[dict[str, str]], output_dir: Path) -> None:
    """Plot the one-run driver income distribution used in the report."""

    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        algorithm = row["algorithm"]
        # Keep only the main PPO config.
        if algorithm == "PPO" and row.get("alpha") not in {"0.2", "0.20000000000000001"}:
            continue
        if algorithm == "PPO":
            algorithm = f"PPO (alpha={DEFAULT_CONFIG.primary_alpha})"
        grouped[algorithm].append(_float(row, "income"))

    plt.figure(figsize=(6, 4))
    for algorithm, values in grouped.items():
        sorted_values = sorted(values)
        if not sorted_values:
            continue
        y_values = [(index + 1) / len(sorted_values) for index in range(len(sorted_values))]
        plt.step(sorted_values, y_values, where="post", label=algorithm)
    plt.xlabel("Driver income")
    plt.ylabel("CDF")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "shock_income_cdf.png")
    plt.close()


def main() -> None:
    default_results_dir = PROJECT_ROOT / "results"
    default_figures_dir = PROJECT_ROOT / "figures"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--baseline-results",
        type=Path,
        default=default_results_dir / "baseline_results.csv",
    )
    parser.add_argument(
        "--ppo-results",
        type=Path,
        default=default_results_dir / "ppo_results.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=default_figures_dir,
    )
    parser.add_argument(
        "--baseline-incomes",
        type=Path,
        default=default_results_dir / "baseline_shock_incomes.csv",
    )
    parser.add_argument(
        "--ppo-incomes",
        type=Path,
        default=default_results_dir / "ppo_shock_incomes.csv",
    )
    args = parser.parse_args()

    baseline_rows = read_rows(args.baseline_results)
    ppo_rows = read_rows(args.ppo_results)
    # Merge rollout summaries for the bar charts.
    all_rows = baseline_rows + ppo_rows
    # Merge shock incomes for the CDF.
    income_rows = read_rows(args.baseline_incomes) + read_rows(args.ppo_incomes)

    plot_revenue_by_scene(all_rows, args.output_dir)
    plot_gini_by_scene(all_rows, args.output_dir)
    plot_alpha_tradeoff(all_rows, args.output_dir)
    plot_income_cdf(income_rows, args.output_dir)


if __name__ == "__main__":
    main()
