from __future__ import annotations
import pandas as pd

def binary_metrics(df: pd.DataFrame) -> dict[str, float]:
    required = {"expected", "predicted"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    tp = int(((df.expected == 1) & (df.predicted == 1)).sum())
    fp = int(((df.expected == 0) & (df.predicted == 1)).sum())
    fn = int(((df.expected == 1) & (df.predicted == 0)).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}
