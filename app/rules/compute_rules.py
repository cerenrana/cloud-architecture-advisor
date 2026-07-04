from app.rules.base import Rule
from app.rules.engine import evaluate_rules
from app.schemas.recommendation import Recommendation
from app.schemas.workload import WorkloadRequest


class GpuComputeRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.gpu_required

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="GPU-accelerated instances with containerized deployment.",
            reason="The workload explicitly requires GPU support, so compute must support accelerated training or inference.",
            tradeoffs="Higher cost and operational complexity, but necessary for GPU workloads.",
            details={"compute_type": "gpu_instance", "deployment_model": "container"},
        )


class HighTrafficComputeRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.daily_users >= 5000 or workload.traffic_level == "high"

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="Autoscaling VM cluster behind a load balancer.",
            reason="High traffic demands horizontal scaling and traffic distribution for stability.",
            tradeoffs="More infrastructure overhead than a single instance, but improves availability and performance.",
            details={"scaling_strategy": "horizontal", "load_balancer": "required"},
        )


class HighResourceComputeRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.cpu >= 8 or workload.ram_gb >= 32

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="Compute-optimized managed instances with vertical and horizontal scaling plans.",
            reason="The requested CPU or memory footprint is large enough to justify dedicated performance capacity.",
            tradeoffs="Better performance isolation, but higher baseline cost than small general-purpose instances.",
            details={
                "compute_type": "compute_optimized",
                "cpu": str(workload.cpu),
                "ram_gb": str(workload.ram_gb),
            },
        )


class BudgetOptimizedComputeRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.budget == "low"

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="General-purpose VM with reserved capacity and cost controls.",
            reason="A low budget means favoring predictable, economical compute over premium instance types.",
            tradeoffs="Less headroom for bursty workloads but lower predictable monthly cost.",
            details={"compute_type": "general_purpose", "cost_profile": "low"},
        )


def recommend_compute(workload: WorkloadRequest) -> Recommendation:
    rules = [
        GpuComputeRule(),
        HighTrafficComputeRule(),
        HighResourceComputeRule(),
        BudgetOptimizedComputeRule(),
    ]
    default = Recommendation(
        recommendation="Balanced general-purpose compute with room for growth.",
        reason="The workload is moderate and can be served by standard compute resources.",
        tradeoffs="This is a safe default but may not be optimal for highly specialized workloads.",
        details={"compute_type": "balanced"},
    )
    return evaluate_rules(workload, rules, default)
