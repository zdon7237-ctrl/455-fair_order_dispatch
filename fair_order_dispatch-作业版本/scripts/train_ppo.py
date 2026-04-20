from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys
from tqdm.auto import tqdm

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from fair_dispatch.config import DEFAULT_CONFIG, DispatchConfig
from fair_dispatch.environment import FairDispatchEnv


RESULT_FIELDS = [
    "algorithm",
    "scene",
    "alpha",
    "episode_revenue",
    "final_episode_gini",
    "final_episode_bottom20_income_mean",
    "mean_completion_rate",
]


def _load_ppo():
    try:
        from stable_baselines3 import PPO
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "stable-baselines3 is required to train PPO. Install project dependencies first."
        ) from exc
    return PPO


def load_shock_multiplier(calibration_path: Path) -> int:
    if not calibration_path.exists():
        return DEFAULT_CONFIG.shock_multiplier
    payload = json.loads(calibration_path.read_text(encoding="utf-8"))
    return int(payload["frozen_multiplier"])


def train_and_evaluate_ppo(
    *,
    alpha: float,
    scene: str,
    total_timesteps: int,
    seed: int,
    shock_multiplier: int,
    config: DispatchConfig = DEFAULT_CONFIG,
    show_progress: bool = True,
) -> tuple[dict[str, float | str], list[float]]:
    PPO = _load_ppo()
    from stable_baselines3.common.callbacks import BaseCallback

    env = FairDispatchEnv(
        config=config,
        scene=scene,
        alpha=alpha,
        shock_multiplier=shock_multiplier,
    )

    # 创建进度条回调
    class TqdmCallback(BaseCallback):
        def __init__(self, total_timesteps: int, desc: str = "Training"):
            super().__init__()
            self.pbar = None
            self.total_timesteps = total_timesteps
            self.desc = desc

        def _on_training_start(self) -> None:
            if show_progress:
                self.pbar = tqdm(total=self.total_timesteps, desc=self.desc, leave=False, mininterval=20.0)

        def _on_step(self) -> bool:
            if self.pbar:
                self.pbar.update(1)
            return True

        def _on_training_end(self) -> None:
            if self.pbar:
                self.pbar.close()

    model = PPO("MlpPolicy", env, verbose=0, seed=seed)
    callback = TqdmCallback(total_timesteps, desc=f"PPO α={alpha} {scene}")
    model.learn(total_timesteps=total_timesteps, callback=callback)

    observation, info = env.reset(seed=seed)
    completion_rates: list[float] = []
    terminated = False

    while not terminated:
        action, _state = model.predict(observation, deterministic=True)
        observation, _reward, terminated, _truncated, info = env.step(action)
        completion_rates.append(info["completion_rate"])

    row = {
        "algorithm": "PPO",
        "scene": scene,
        "alpha": alpha,
        "episode_revenue": info["episode_revenue"],
        "final_episode_gini": info["current_gini"],
        "final_episode_bottom20_income_mean": info["bottom20_income_mean"],
        "mean_completion_rate": sum(completion_rates) / max(1, len(completion_rates)),
    }
    return row, env.cumulative_income.astype(float).tolist()


def write_results(rows: list[dict[str, float | str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_income_snapshot(
    rows_with_incomes: list[tuple[dict[str, float | str], list[float]]], output_path: Path
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["algorithm", "scene", "alpha", "driver_index", "income"],
        )
        writer.writeheader()
        for row, incomes in rows_with_incomes:
            if row["scene"] != "shock":
                continue
            for driver_index, income in enumerate(incomes):
                writer.writerow(
                    {
                        "algorithm": row["algorithm"],
                        "scene": row["scene"],
                        "alpha": row["alpha"],
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
        default=default_results_dir / "ppo_results.csv",
    )
    parser.add_argument(
        "--income-output",
        type=Path,
        default=default_results_dir / "ppo_shock_incomes.csv",
    )
    parser.add_argument(
        "--calibration-input",
        type=Path,
        default=default_results_dir / "shock_calibration.json",
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--total-timesteps", type=int, default=20000)
    args = parser.parse_args()

    rows_with_incomes: list[tuple[dict[str, float | str], list[float]]] = []
    shock_multiplier = load_shock_multiplier(args.calibration_input)

    experiments = [
        (alpha, scene)
        for alpha in DEFAULT_CONFIG.alpha_grid
        for scene in ("normal", "shock")
    ]

    for alpha, scene in tqdm(experiments, desc="训练 PPO", unit="exp"):
        rows_with_incomes.append(
            train_and_evaluate_ppo(
                alpha=alpha,
                scene=scene,
                total_timesteps=args.total_timesteps,
                seed=args.seed,
                shock_multiplier=shock_multiplier,
                show_progress=True,
            )
        )

    rows = [row for row, _incomes in rows_with_incomes]
    write_results(rows, args.output)
    write_income_snapshot(rows_with_incomes, args.income_output)
    print(f"Wrote {len(rows)} PPO result rows to {args.output}.")


if __name__ == "__main__":
    main()
