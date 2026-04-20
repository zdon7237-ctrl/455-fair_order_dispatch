import json
from pathlib import Path


NOTEBOOK_PATH = Path(__file__).resolve().parents[1] / "final_submission_cn.ipynb"


def _load_notebook() -> dict:
    return json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))


def test_chinese_notebook_exists_and_has_core_sections():
    assert NOTEBOOK_PATH.exists()

    notebook = _load_notebook()
    full_text = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    required_sections = [
        "# 需求冲击下订单派单的效率与公平",
        "## 摘要",
        "## 问题设定",
        "## 环境设计",
        "## 基线方法与 PPO",
        "## 评价指标",
        "## 主要结果",
        "## 结论",
        "## 参考文献",
    ]

    for section in required_sections:
        assert section in full_text


def test_chinese_notebook_is_submission_ready():
    notebook = _load_notebook()
    full_text = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert "Insert the four required figures here" not in full_text
    assert "episode_revenue_by_scene.png" in full_text
    assert "final_gini_by_scene.png" in full_text
    assert "shock_income_cdf.png" in full_text
    assert "alpha_tradeoff.png" in full_text
    assert "shock multiplier" not in full_text


def test_chinese_notebook_is_self_contained():
    notebook = _load_notebook()
    full_text = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert "from fair_dispatch" not in full_text
    assert "class DispatchConfig" in full_text
    assert "def gini_coefficient" in full_text
    assert "def local_first_policy" in full_text
    assert "def build_normal_demand_schedule" in full_text
    assert "class FairDispatchEnv" in full_text
    assert "def train_and_evaluate_ppo" in full_text
