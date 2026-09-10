"""Deterministic exact-match evaluation; no invented baseline numbers."""
from collections.abc import Sequence


def exact_match(expected: Sequence[object], actual: Sequence[object]) -> dict:
    if not expected or len(expected) != len(actual):
        raise ValueError("Evaluation requires nonempty, equally sized sequences")
    correct = sum(a == b for a, b in zip(expected, actual))
    return {"cases": len(expected), "correct": correct,
            "accuracy": correct / len(expected)}
