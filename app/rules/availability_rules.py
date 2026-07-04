from app.rules.base import Rule
from app.rules.engine import evaluate_rules
from app.schemas.recommendation import Recommendation
from app.schemas.workload import WorkloadRequest


class HighAvailabilityRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.availability == "high"

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="Multi-AZ deployment with automatic failover and health checks.",
            reason="High availability requirements demand redundancy and fast recovery.",
            tradeoffs="Higher infrastructure cost and more complex deployment, but greatly improved uptime.",
            details={"availability_model": "multi_az", "failover": "automatic"},
        )


class MediumAvailabilityRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.availability == "medium"

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="Single region deployment with redundancy and monitoring.",
            reason="Medium availability needs can be met with regional redundancy and alerting.",
            tradeoffs="Lower cost than multi-AZ but still requires some failover planning.",
            details={"availability_model": "regional", "monitoring": "enabled"},
        )


def recommend_availability(workload: WorkloadRequest) -> Recommendation:
    rules = [HighAvailabilityRule(), MediumAvailabilityRule()]
    default = Recommendation(
        recommendation="Single-zone deployment with basic recovery procedures.",
        reason="Low availability requirements allow a simpler, more cost-effective design.",
        tradeoffs="Lower operational cost at the expense of longer recovery windows.",
        details={"availability_model": "single_zone"},
    )
    return evaluate_rules(workload, rules, default)
