from app.rules.base import Rule
from app.rules.engine import evaluate_rules
from app.schemas.recommendation import Recommendation
from app.schemas.workload import WorkloadRequest


class HighCapacityStorageRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.storage_gb >= 1000 or workload.traffic_level == "high"

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="Distributed object storage with lifecycle management.",
            reason="Large storage needs and high traffic benefit from scalable object storage.",
            tradeoffs="Higher latency for some workloads compared to block storage, but much better scalability and cost efficiency.",
            details={"storage_type": "object", "management": "lifecycle"},
        )


class CostSensitiveStorageRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.budget == "low"

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="Standard block storage with reserved IOPS.",
            reason="For cost-sensitive workloads, simpler block storage reduces operational expense.",
            tradeoffs="Smaller scalability envelope than object storage but lower baseline cost.",
            details={"storage_type": "block", "cost_profile": "low"},
        )


class HighlyAvailableStorageRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.availability == "high"

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="Replicated managed storage with snapshots, backups, and cross-zone recovery.",
            reason="High availability workloads need durable storage and fast recovery paths.",
            tradeoffs="More expensive than single-zone storage, but reduces data-loss and downtime risk.",
            details={
                "storage_type": "replicated_managed",
                "snapshots": "enabled",
                "recovery": "cross_zone",
            },
        )


def recommend_storage(workload: WorkloadRequest) -> Recommendation:
    rules = [
        HighCapacityStorageRule(),
        HighlyAvailableStorageRule(),
        CostSensitiveStorageRule(),
    ]
    default = Recommendation(
        recommendation="Managed block storage with snapshots and redundancy.",
        reason="This is a balanced choice for most applications requiring reliable storage.",
        tradeoffs="Less cost-efficient for extremely large datasets than object storage.",
        details={"storage_type": "managed_block"},
    )
    return evaluate_rules(workload, rules, default)
