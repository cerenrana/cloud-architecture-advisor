from typing import Sequence
from app.rules.base import Rule
from app.schemas.recommendation import Recommendation
from app.schemas.workload import WorkloadRequest


def evaluate_rules(
    workload: WorkloadRequest,
    rules: Sequence[Rule],
    default: Recommendation,
) -> Recommendation:
    for rule in rules:
        if rule.applies_to(workload):
            return rule.recommend(workload)
    return default
