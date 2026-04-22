#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Summarize multi-seed results and plot error bars."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

# Use project-local imports.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from fair_dispatch.config import DEFAULT_CONFIG

# Keep Chinese labels visible.
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def load_results(file_path: Path) -> pd.DataFrame:
    """Load the experiment rows."""
    if not file_path.exists():
        raise FileNotFoundError(f"结果文件不存在: {file_path}")

    df = pd.read_csv(file_path)
    print(f"成功加载 {len(df)} 条实验记录")
    return df


def compute_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate mean, std, and sem."""
    # Group by algorithm and scene.
    group_keys = ['algorithm', 'scene']

    # Add alpha only for PPO.
    if 'alpha' in df.columns:
        # Leave baseline alpha empty.
        df_copy = df.copy()
        df_copy.loc[df_copy['algorithm'] != 'PPO', 'alpha'] = None
        group_keys.append('alpha')
    else:
        df_copy = df

    # Collect summary stats.
    stats_list = []

    for group_name, group_df in df_copy.groupby(group_keys, dropna=False):
        if isinstance(group_name, tuple):
            if len(group_keys) == 3:
                algorithm, scene, alpha = group_name
            else:
                algorithm, scene = group_name
                alpha = None
        else:
            algorithm = group_name
            scene = None
            alpha = None

        stats = {
            'algorithm': algorithm,
            'scene': scene,
        }

        if alpha is not None:
            stats['alpha'] = alpha

        # Revenue summary.
        if 'episode_revenue' in group_df.columns:
            stats['revenue_mean'] = group_df['episode_revenue'].mean()
            stats['revenue_std'] = group_df['episode_revenue'].std()
            stats['revenue_sem'] = group_df['episode_revenue'].sem()

        # Fairness summary.
        if 'final_episode_gini' in group_df.columns:
            stats['gini_mean'] = group_df['final_episode_gini'].mean()
            stats['gini_std'] = group_df['final_episode_gini'].std()
            stats['gini_sem'] = group_df['final_episode_gini'].sem()

        # Sample count.
        stats['n_samples'] = len(group_df)

        stats_list.append(stats)

    summary_df = pd.DataFrame(stats_list)
    print(f"\n计算了 {len(summary_df)} 个组合的统计量")
    return summary_df


def significance_tests(df: pd.DataFrame, alpha_value: float = 0.2) -> pd.DataFrame:
    """Compare PPO against the baselines."""
    results = []

    # Pick one PPO alpha.
    if 'alpha' in df.columns:
        ppo_df = df[(df['algorithm'] == 'PPO') & (df['alpha'].astype(float).round(1) == alpha_value)]
    else:
        ppo_df = df[df['algorithm'] == 'PPO']

    # Fixed baselines.
    baseline_algorithms = ['Local-First', 'Demand-Greedy']

    # Check every scene.
    scenes = df['scene'].unique()

    # Test the available metrics.
    metrics = []
    if 'episode_revenue' in df.columns:
        metrics.append(('episode_revenue', '平台收入'))
    if 'final_episode_gini' in df.columns:
        metrics.append(('final_episode_gini', '基尼系数'))

    for scene in scenes:
        ppo_scene = ppo_df[ppo_df['scene'] == scene]

        for baseline in baseline_algorithms:
            baseline_scene = df[(df['algorithm'] == baseline) & (df['scene'] == scene)]

            if len(ppo_scene) == 0 or len(baseline_scene) == 0:
                print(f"警告: {scene} 场景下 PPO 或 {baseline} 数据为空，跳过检验")
                continue

            for metric_col, metric_name in metrics:
                ppo_values = ppo_scene[metric_col].values
                baseline_values = baseline_scene[metric_col].values

                # Two-sample t-test.
                t_stat, p_value = ttest_ind(ppo_values, baseline_values)

                # Cohen's d.
                pooled_std = np.sqrt(
                    ((len(ppo_values) - 1) * np.var(ppo_values, ddof=1) +
                     (len(baseline_values) - 1) * np.var(baseline_values, ddof=1)) /
                    (len(ppo_values) + len(baseline_values) - 2)
                )
                cohens_d = (np.mean(ppo_values) - np.mean(baseline_values)) / pooled_std if pooled_std > 0 else 0

                results.append({
                    'scene': scene,
                    'metric': metric_name,
                    'comparison': f'PPO(α={alpha_value}) vs {baseline}',
                    'ppo_mean': np.mean(ppo_values),
                    'ppo_std': np.std(ppo_values, ddof=1),
                    'baseline_mean': np.mean(baseline_values),
                    'baseline_std': np.std(baseline_values, ddof=1),
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'cohens_d': cohens_d,
                    'significant': 'Yes' if p_value < 0.05 else 'No',
                    'ppo_n': len(ppo_values),
                    'baseline_n': len(baseline_values),
                })

    test_df = pd.DataFrame(results)
    print(f"\n完成 {len(test_df)} 项显著性检验")
    return test_df


def plot_with_error_bars(summary_df: pd.DataFrame, output_dir: Path) -> None:
    """Build the summary figures."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Keep the main PPO setting.
    primary_df = summary_df.copy()
    if 'alpha' in primary_df.columns:
        primary_df = primary_df[
            (primary_df['algorithm'] != 'PPO') |
            (primary_df['alpha'].astype(float).round(1) == 0.2)
        ]

    # Revenue bars.
    if 'revenue_mean' in primary_df.columns:
        plot_revenue_comparison(primary_df, output_dir)

    # Gini bars.
    if 'gini_mean' in primary_df.columns:
        plot_gini_comparison(primary_df, output_dir)

    # Alpha trade-off plot.
    if 'alpha' in summary_df.columns:
        ppo_df = summary_df[summary_df['algorithm'] == 'PPO']
        if len(ppo_df) > 0:
            plot_alpha_tradeoff_with_errors(ppo_df, output_dir)

    print(f"\n图表已保存到 {output_dir}")


def plot_revenue_comparison(df: pd.DataFrame, output_dir: Path) -> None:
    """Plot revenue with error bars."""
    scenes = df['scene'].unique()
    algorithms = df[df['scene'] == scenes[0]]['algorithm'].unique()

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(algorithms))
    width = 0.35

    for i, scene in enumerate(scenes):
        scene_df = df[df['scene'] == scene].sort_values('algorithm')
        means = scene_df['revenue_mean'].values
        errors = scene_df['revenue_sem'].values

        offset = width * (i - len(scenes) / 2 + 0.5)
        ax.bar(x + offset, means, width, yerr=errors,
               label=f'{scene}场景', capsize=5, alpha=0.8)

    ax.set_xlabel('算法', fontsize=12)
    ax.set_ylabel('平台收入', fontsize=12)
    ax.set_title('不同场景下的平台收入对比', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'episode_revenue_by_scene.png', dpi=300)
    plt.close()
    print("  ✓ 已生成: episode_revenue_by_scene.png")


def plot_gini_comparison(df: pd.DataFrame, output_dir: Path) -> None:
    """Plot Gini with error bars."""
    scenes = df['scene'].unique()
    algorithms = df[df['scene'] == scenes[0]]['algorithm'].unique()

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(algorithms))
    width = 0.35

    for i, scene in enumerate(scenes):
        scene_df = df[df['scene'] == scene].sort_values('algorithm')
        means = scene_df['gini_mean'].values
        errors = scene_df['gini_sem'].values

        offset = width * (i - len(scenes) / 2 + 0.5)
        ax.bar(x + offset, means, width, yerr=errors,
               label=f'{scene}场景', capsize=5, alpha=0.8)

    ax.set_xlabel('算法', fontsize=12)
    ax.set_ylabel('基尼系数', fontsize=12)
    ax.set_title('不同场景下的公平性对比（基尼系数）', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'final_gini_by_scene.png', dpi=300)
    plt.close()
    print("  ✓ 已生成: final_gini_by_scene.png")


def plot_alpha_tradeoff_with_errors(ppo_df: pd.DataFrame, output_dir: Path) -> None:
    """Plot the PPO trade-off curve."""
    # Only use shock runs.
    shock_df = ppo_df[ppo_df['scene'] == 'shock'].copy()

    if len(shock_df) == 0:
        print("  警告: 没有shock场景的PPO数据，跳过alpha权衡图")
        return

    shock_df = shock_df.sort_values('alpha')

    fig, ax = plt.subplots(figsize=(8, 6))

    for _, row in shock_df.iterrows():
        ax.errorbar(
            row['gini_mean'],
            row['revenue_mean'],
            xerr=row['gini_sem'],
            yerr=row['revenue_sem'],
            fmt='o',
            markersize=8,
            capsize=5,
            label=f"α={row['alpha']:.1f}"
        )

    ax.set_xlabel('基尼系数（公平性）', fontsize=12)
    ax.set_ylabel('平台收入（效率）', fontsize=12)
    ax.set_title('PPO算法的效率-公平性权衡（shock场景）', fontsize=14, fontweight='bold')
    ax.legend(title='Alpha参数')
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'alpha_tradeoff.png', dpi=300)
    plt.close()
    print("  ✓ 已生成: alpha_tradeoff.png")


def main() -> None:
    """CLI entry point."""
    # Default paths.
    default_results_dir = PROJECT_ROOT / "results"
    default_figures_dir = PROJECT_ROOT / "figures"

    # Parse CLI args.
    parser = argparse.ArgumentParser(
        description='对多种子实验结果进行统计分析和显著性检验'
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=default_results_dir / 'multi_seed_results.csv',
        help='输入的多种子实验结果CSV文件'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=default_results_dir,
        help='统计结果输出目录'
    )
    parser.add_argument(
        '--figures-dir',
        type=Path,
        default=default_figures_dir,
        help='图表输出目录'
    )
    parser.add_argument(
        '--alpha',
        type=float,
        default=0.2,
        help='PPO的alpha参数值（用于显著性检验）'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("统计分析脚本")
    print("=" * 60)

    try:
        # 1. Load the rows.
        print("\n[1/5] 加载实验结果...")
        df = load_results(args.input)
        print(f"  数据形状: {df.shape}")
        print(f"  列名: {list(df.columns)}")

        # 2. Aggregate stats.
        print("\n[2/5] 计算统计量...")
        summary_df = compute_statistics(df)

        # Save the summary.
        summary_path = args.output_dir / 'statistical_summary.csv'
        summary_df.to_csv(summary_path, index=False, encoding='utf-8-sig')
        print(f"  ✓ 统计汇总已保存: {summary_path}")

        # 3. Run the tests.
        print("\n[3/5] 进行显著性检验...")
        test_df = significance_tests(df, alpha_value=args.alpha)

        # Save the test output.
        test_path = args.output_dir / 'significance_tests.csv'
        test_df.to_csv(test_path, index=False, encoding='utf-8-sig')
        print(f"  ✓ 显著性检验结果已保存: {test_path}")

        # Print the headline results.
        print("\n  关键发现:")
        for _, row in test_df.iterrows():
            sig_mark = "***" if row['p_value'] < 0.001 else "**" if row['p_value'] < 0.01 else "*" if row['p_value'] < 0.05 else ""
            print(f"    {row['scene']} - {row['metric']}: {row['comparison']}")
            print(f"      t={row['t_statistic']:.3f}, p={row['p_value']:.4f} {sig_mark}, d={row['cohens_d']:.3f}")

        # 4. Draw the figures.
        print("\n[4/5] 绘制带误差棒的图表...")
        plot_with_error_bars(summary_df, args.figures_dir)

        # 5. Finish up.
        print("\n[5/5] 分析完成!")
        print("=" * 60)
        print(f"\n输出文件:")
        print(f"  - 统计汇总: {summary_path}")
        print(f"  - 显著性检验: {test_path}")
        print(f"  - 图表目录: {args.figures_dir}")
        print("\n" + "=" * 60)

    except FileNotFoundError as e:
        print(f"\n错误: {e}")
        print("\n提示: 请先运行多种子实验脚本生成 multi_seed_results.csv")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
