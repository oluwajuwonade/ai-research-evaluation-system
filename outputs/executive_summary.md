# Executive Summary — Illustrative AI Research Evaluation

**Scope:** Claim-level evaluation fixture for three fictional research workflows. Metrics are illustrative and do not measure a deployed AI system.

## Headline results

- Highest F1 workflow: **reviewed at 100.0%**.
- Best workflow citation coverage: **100.0%**.
- Evaluated claims: **12** across **3 workflows**.

## Decision readout

The fast workflow is cheaper and faster but sacrifices recall in this fixture. The reviewed workflow has the strongest quality result at higher latency and cost. A production decision should set minimum quality thresholds before optimizing for speed or cost.

## Controls and limitations

Precision, recall, and F1 are calculated from explicit expected and predicted labels. Citation presence is tracked separately from claim correctness. This synthetic fixture does not assess source quality, citation entailment, claim severity, or evaluator agreement.
