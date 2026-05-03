import json
from pathlib import Path


NOTEBOOK_PATH = Path(__file__).resolve().parents[1] / "final_submission_en.ipynb"


def _load_notebook() -> dict:
    return json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))


def test_notebook_has_required_sections():
    notebook = _load_notebook()
    full_text = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    required_sections = [
        "# Efficiency and Fairness in Order Dispatch Under Demand Shock",
        "## Abstract",
        "## Problem Setup",
        "## Environment",
        "## Baselines and PPO",
        "## Metrics",
        "## Results",
        "## Conclusion",
        "## References",
    ]

    for section in required_sections:
        assert section in full_text


def test_notebook_results_section_is_not_placeholder_only():
    notebook = _load_notebook()
    full_text = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert "Insert the four required figures here" not in full_text
    assert "episode_revenue_by_scene.png" in full_text
    assert "final_gini_by_scene.png" in full_text
    assert "shock_income_cdf.png" in full_text
    assert "alpha_tradeoff.png" in full_text
