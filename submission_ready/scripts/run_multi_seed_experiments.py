#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run multi-seed baseline and PPO experiments."""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import sys
from typing import Any

import numpy as np
from tqdm.auto import tqdm

# Let PyTorch pick the device.
# os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Leave this off.

# Use project-local imports.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from fair_dispatch.baselines import demand_greedy_logits, local_first_logits
from fair_dispatch.config import DEFAULT_CONFIG, DispatchConfig
from fair_dispatch.environment import FairDispatchEnv


# Experiment config
SEEDS = [0, 42, 123, 456, 789]

SCENES = ["normal", "shock"]

BASELINE_ALGORITHMS = ["Local-First", "Demand-Greedy"]

ALPHA_VALUES = [0.0, 0.1, 0.2, 0.4]

RESULT_FIELDS = [
    "seed",
    "algorithm",
    "scene",
    "alpha",
    "episode_revenue",
    "final_episode_gini",
    "final_episode_bottom20_income_mean",
    "mean_completion_rate",
]


def _load_ppo():
    """Load PPO lazily."""
    try:
        from stable_baselines3 import PPO
    except ImportError as exc:
        raise RuntimeError(
            "需要安装 stable-baselines3 才能训练 PPO。请先安装项目依赖。"
        ) from exc
    return PPO


def load_shock_multiplier(calibration_path: Path) -> int:
    """Read the frozen shock level."""
    if not calibration_path.exists():
        return DEFAULT_CONFIG.shock_multiplier
    payload = json.loads(calibration_path.read_text(encoding="utf-8"))
    return int(payload["frozen_multiplier"])


def run_baseline(
    policy_name: str,
    scene: str,
    seed: int,
    *,
    config: DispatchConfig = DEFAULT_CONFIG,
    shock_multiplier: int | None = None,
) -> dict[str, Any]:
    """Run one baseline rollout."""
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
        demand = observation[config.zone_count : config.zone_count * 2]
        if policy_name == "Local-First":
            action = local_first_logits(demand)
        elif policy_name == "Demand-Greedy":
            action = demand_greedy_logits(demand)
        else:
            raise ValueError(f"不支持的基线算法: {policy_name}")

        observation, _reward, terminated, _truncated, info = env.step(action)
        completion_rates.append(info["completion_rate"])

    return {
        "seed": seed,
        "algorithm": policy_name,
        "scene": scene,
        "alpha": "",
        "episode_revenue": info["episode_revenue"],
        "final_episode_gini": info["current_gini"],
        "final_episode_bottom20_income_mean": info["bottom20_income_mean"],
        "mean_completion_rate": float(np.mean(completion_rates)),
    }


def run_ppo(
    alpha: float,
    scene: str,
    seed: int,
    *,
    total_timesteps: int,
    shock_multiplier: int,
    config: DispatchConfig = DEFAULT_CONFIG,
    show_progress: bool = True,
) -> dict[str, Any]:
    """Train and score one PPO run."""
    PPO = _load_ppo()
    from stable_baselines3.common.callbacks import BaseCallback

    # Build the env once.
    env = FairDispatchEnv(
        config=config,
        scene=scene,
        alpha=alpha,
        shock_multiplier=shock_multiplier,
    )

    # Keep the progress bar light.
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

    # Train first.
    model = PPO("MlpPolicy", env, verbose=0, seed=seed, device="auto")
    callback = TqdmCallback(total_timesteps, desc=f"PPO α={alpha} {scene}")
    model.learn(total_timesteps=total_timesteps, callback=callback)

    # Then score one episode.
    observation, info = env.reset(seed=seed)
    completion_rates: list[float] = []
    terminated = False

    while not terminated:
        action, _state = model.predict(observation, deterministic=True)
        observation, _reward, terminated, _truncated, info = env.step(action)
        completion_rates.append(info["completion_rate"])

    return {
        "seed": seed,
        "algorithm": "PPO",
        "scene": scene,
        "alpha": alpha,
        "episode_revenue": info["episode_revenue"],
        "final_episode_gini": info["current_gini"],
        "final_episode_bottom20_income_mean": info["bottom20_income_mean"],
        "mean_completion_rate": float(np.mean(completion_rates)),
    }


def run_all_experiments(
    *,
    total_timesteps: int = 20000,
    calibration_path: Path | None = None,
    config: DispatchConfig = DEFAULT_CONFIG,
) -> list[dict[str, Any]]:
    """Run the full seed sweep."""
    # Load the frozen shock level.
    if calibration_path and calibration_path.exists():
        shock_multiplier = load_shock_multiplier(calibration_path)
    else:
        shock_multiplier = config.shock_multiplier

    print(f"使用 shock_multiplier = {shock_multiplier}")
    print(f"随机种子: {SEEDS}")
    print(f"场景: {SCENES}")
    print(f"基线算法: {BASELINE_ALGORITHMS}")
    print(f"PPO alpha 值: {ALPHA_VALUES}")
    print()

    # Count the workload.
    baseline_count = len(BASELINE_ALGORITHMS) * len(SCENES) * len(SEEDS)
    ppo_count = len(ALPHA_VALUES) * len(SCENES) * len(SEEDS)
    total_count = baseline_count + ppo_count

    print(f"总实验数: {total_count}")
    print(f"  - 基线实验: {baseline_count}")
    print(f"  - PPO 实验: {ppo_count}")
    print()

    results = []

    # Baseline sweep.
    print("=" * 70)
    print("开始运行基线算法实验")
    print("=" * 70)

    baseline_experiments = [
        (seed, scene, algorithm)
        for seed in SEEDS
        for scene in SCENES
        for algorithm in BASELINE_ALGORITHMS
    ]

    for seed, scene, algorithm in tqdm(baseline_experiments, desc="基线实验", unit="exp"):
        result = run_baseline(
            policy_name=algorithm,
            scene=scene,
            seed=seed,
            config=config,
            shock_multiplier=shock_multiplier if scene == "shock" else None,
        )
        results.append(result)

    # PPO sweep.
    print()
    print("=" * 70)
    print("开始运行 PPO 实验")
    print("=" * 70)

    ppo_experiments = [
        (seed, scene, alpha)
        for seed in SEEDS
        for scene in SCENES
        for alpha in ALPHA_VALUES
    ]

    for seed, scene, alpha in tqdm(ppo_experiments, desc="PPO 实验", unit="exp"):
        result = run_ppo(
            alpha=alpha,
            scene=scene,
            seed=seed,
            total_timesteps=total_timesteps,
            shock_multiplier=shock_multiplier,
            config=config,
            show_progress=True,
        )
        results.append(result)

    print()
    print("=" * 70)
    print("所有实验完成！")
    print("=" * 70)

    return results


def write_results(results: list[dict[str, Any]], output_path: Path) -> None:
    """Write rows to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(results)
    print(f"结果已保存到: {output_path}")

def main() -> None:
    """CLI entry point."""
    default_results_dir = PROJECT_ROOT / "results"

    parser = argparse.ArgumentParser(description="运行多种子实验")
    parser.add_argument(
        "--output",
        type=Path,
        default=default_results_dir / "multi_seed_results.csv",
        help="输出 CSV 文件路径",
    )
    parser.add_argument(
        "--calibration-input",
        type=Path,
        default=default_results_dir / "shock_calibration.json",
        help="校准文件路径",
    )
    parser.add_argument(
        "--total-timesteps",
        type=int,
        default=20000,
        help="PPO 训练总步数",
    )
    args = parser.parse_args()

    print("=" * 70)
    print("多种子实验脚本")
    print("=" * 70)
    print(f"输出文件: {args.output}")
    print(f"校准文件: {args.calibration_input}")
    print(f"PPO 训练步数: {args.total_timesteps}")

    # Show the detected device.
    try:
        import torch
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            print(f"设备: GPU ({device_name})")
        else:
            print(f"设备: CPU (GPU 不可用)")
    except ImportError:
        print(f"设备: CPU (PyTorch 未安装)")
    print()

    # Run the sweep.
    results = run_all_experiments(
        total_timesteps=args.total_timesteps,
        calibration_path=args.calibration_input,
    )

    # Save the rows.
    write_results(results, args.output)

    print()
    print(f"共完成 {len(results)} 个实验")


if __name__ == "__main__":
    main()
