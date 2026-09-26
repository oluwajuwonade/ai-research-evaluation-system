from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from evaluate import binary_metrics

ROOT = Path(__file__).resolve().parents[1]
DATA, OUTPUTS = ROOT / "data", ROOT / "outputs"
DATA.mkdir(exist_ok=True); OUTPUTS.mkdir(exist_ok=True)


def main() -> None:
    claims = pd.DataFrame({
        "claim_id": range(1, 13),
        "workflow": ["standard"] * 4 + ["fast"] * 4 + ["reviewed"] * 4,
        "expected": [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        "predicted": [1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
        "citation_present": [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        "latency_seconds": [42, 38, 35, 46, 18, 16, 15, 21, 55, 49, 51, 58],
        "cost_usd": [0.18, 0.15, 0.14, 0.21, 0.07, 0.06, 0.05, 0.08, 0.24, 0.22, 0.23, 0.27],
    })
    claims.to_csv(DATA / "illustrative_claim_evaluation.csv", index=False)
    rows = []
    for workflow, group in claims.groupby("workflow", sort=False):
        metrics = binary_metrics(group[["expected", "predicted"]])
        rows.append({"workflow": workflow, **metrics, "citation_coverage": group.citation_present.mean(), "avg_latency_seconds": group.latency_seconds.mean(), "avg_cost_usd": group.cost_usd.mean(), "claims_evaluated": len(group)})
    scorecard = pd.DataFrame(rows)
    scorecard.to_csv(OUTPUTS / "workflow_scorecard.csv", index=False)
    error_taxonomy = pd.DataFrame({"failure_type": ["False negative", "False positive", "Missing citation", "Correct claim"], "count": [int(((claims.expected == 1) & (claims.predicted == 0)).sum()), int(((claims.expected == 0) & (claims.predicted == 1)).sum()), int((claims.citation_present == 0).sum()), int((claims.expected == claims.predicted).sum())]})
    error_taxonomy.to_csv(OUTPUTS / "failure_taxonomy.csv", index=False)
    best = scorecard.loc[scorecard.f1.idxmax()]
    (OUTPUTS / "executive_summary.md").write_text(f"""# Executive Summary — Illustrative AI Research Evaluation\n\n**Scope:** Claim-level evaluation fixture for three fictional research workflows. Metrics are illustrative and do not measure a deployed AI system.\n\n## Headline results\n\n- Highest F1 workflow: **{best.workflow} at {best.f1:.1%}**.\n- Best workflow citation coverage: **{scorecard.citation_coverage.max():.1%}**.\n- Evaluated claims: **{len(claims)}** across **{claims.workflow.nunique()} workflows**.\n\n## Decision readout\n\nThe fast workflow is cheaper and faster but sacrifices recall in this fixture. The reviewed workflow has the strongest quality result at higher latency and cost. A production decision should set minimum quality thresholds before optimizing for speed or cost.\n\n## Controls and limitations\n\nPrecision, recall, and F1 are calculated from explicit expected and predicted labels. Citation presence is tracked separately from claim correctness. This synthetic fixture does not assess source quality, citation entailment, claim severity, or evaluator agreement.\n""")

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(9, 5.2))
    x = range(len(scorecard)); width = 0.24
    ax.bar([i - width for i in x], scorecard.precision * 100, width, label="Precision", color="#2563EB")
    ax.bar(x, scorecard.recall * 100, width, label="Recall", color="#7C3AED")
    ax.bar([i + width for i in x], scorecard.f1 * 100, width, label="F1", color="#15803D")
    ax.set_xticks(list(x)); ax.set_xticklabels(scorecard.workflow.str.title()); ax.set_ylim(0, 110)
    ax.set_ylabel("Score (%)"); ax.set_title("Illustrative AI Research Quality Scorecard", loc="left", weight="bold"); ax.legend(frameon=False, ncol=3)
    fig.tight_layout(); fig.savefig(OUTPUTS / "quality_scorecard.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.scatter(scorecard.avg_latency_seconds, scorecard.f1 * 100, s=scorecard.avg_cost_usd * 1800, color=["#2563EB", "#C2413B", "#15803D"], alpha=.9)
    for _, row in scorecard.iterrows(): ax.annotate(row.workflow.title(), (row.avg_latency_seconds, row.f1 * 100), xytext=(6, 7), textcoords="offset points")
    ax.set_xlabel("Average latency (seconds)"); ax.set_ylabel("F1 score (%)"); ax.set_title("Quality–Latency–Cost Trade-off", loc="left", weight="bold")
    fig.tight_layout(); fig.savefig(OUTPUTS / "quality_latency_tradeoff.png", dpi=180); plt.close(fig)


if __name__ == "__main__":
    main()
