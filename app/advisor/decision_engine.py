from app.schemas.workload import WorkloadRequest
from app.schemas.recommendation import (
    AlternativeArchitecture,
    CostEstimate,
    RecommendationResponse,
)
from app.rules.compute_rules import recommend_compute
from app.rules.storage_rules import recommend_storage
from app.rules.network_rules import recommend_networking
from app.rules.deployment_rules import recommend_deployment
from app.rules.availability_rules import recommend_availability


class DecisionEngine:
    def generate(self, workload: WorkloadRequest) -> RecommendationResponse:
        architecture = {
            "compute": recommend_compute(workload),
            "storage": recommend_storage(workload),
            "networking": recommend_networking(workload),
            "deployment": recommend_deployment(workload),
            "availability": recommend_availability(workload),
        }

        return RecommendationResponse(
            project_name=workload.project_name,
            recommended_architecture=architecture,
            confidence_score=self._calculate_confidence(workload),
            estimated_monthly_cost=self._estimate_cost(workload),
            alternatives=self._build_alternatives(workload),
            architecture_diagram=self._build_diagram(workload),
        )

    def _calculate_confidence(self, workload: WorkloadRequest) -> float:
        score = 0.62

        if workload.deployment_preference != "no_preference":
            score += 0.08
        if workload.traffic_level in {"low", "medium", "high"}:
            score += 0.06
        if workload.availability in {"low", "medium", "high"}:
            score += 0.06
        if workload.cpu >= 2 and workload.ram_gb >= 4:
            score += 0.05
        if workload.gpu_required or workload.daily_users >= 5000:
            score += 0.05

        return round(min(score, 0.92), 2)

    def _estimate_cost(self, workload: WorkloadRequest) -> CostEstimate:
        base_cost = 35
        compute_cost = workload.cpu * 12 + workload.ram_gb * 3
        storage_cost = max(10, int(workload.storage_gb * 0.08))
        user_cost = max(5, int(workload.daily_users / 1000) * 8)

        traffic_multiplier = {
            "low": 1.0,
            "medium": 1.35,
            "high": 2.1,
        }[workload.traffic_level]
        availability_multiplier = {
            "low": 1.0,
            "medium": 1.25,
            "high": 1.75,
        }[workload.availability]
        budget_multiplier = {
            "low": 0.85,
            "medium": 1.0,
            "high": 1.25,
        }[workload.budget]
        gpu_cost = 180 if workload.gpu_required else 0

        midpoint = int(
            (base_cost + compute_cost + storage_cost + user_cost + gpu_cost)
            * traffic_multiplier
            * availability_multiplier
            * budget_multiplier
        )

        return CostEstimate(
            min_usd=max(20, int(midpoint * 0.8)),
            max_usd=max(35, int(midpoint * 1.25)),
            note="Rough monthly estimate for planning; real provider prices vary by region, usage, and discounts.",
        )

    def _build_alternatives(self, workload: WorkloadRequest) -> list[AlternativeArchitecture]:
        estimate = self._estimate_cost(workload)
        conservative = max(20, int(estimate.min_usd * 0.75))
        balanced = int((estimate.min_usd + estimate.max_usd) / 2)
        performance = max(balanced + 40, int(estimate.max_usd * 1.35))

        return [
            AlternativeArchitecture(
                name="Cost optimized",
                description="Smaller compute footprint, simpler networking, and scheduled scaling.",
                estimated_monthly_cost_usd=conservative,
                best_for="Early-stage projects, prototypes, and low budget workloads.",
            ),
            AlternativeArchitecture(
                name="Balanced",
                description="Managed compute, reliable storage, monitoring, and moderate redundancy.",
                estimated_monthly_cost_usd=balanced,
                best_for="Production applications with steady growth expectations.",
            ),
            AlternativeArchitecture(
                name="Performance focused",
                description="Autoscaling compute, CDN, stronger redundancy, and more operational headroom.",
                estimated_monthly_cost_usd=performance,
                best_for="High traffic, strict availability, or GPU-heavy workloads.",
            ),
        ]

    def _build_diagram(self, workload: WorkloadRequest) -> str:
        compute_node = "GPU Compute" if workload.gpu_required else "App Compute"
        storage_node = "Object Storage" if workload.storage_gb >= 1000 else "Managed Storage"
        entry_node = "CDN" if workload.traffic_level == "high" else "API Gateway"
        availability_node = "Multi-AZ Failover" if workload.availability == "high" else "Monitoring"

        return "\n".join(
            [
                "flowchart LR",
                "  User[Users] --> Edge[" + entry_node + "]",
                "  Edge --> LB[Load Balancer]",
                "  LB --> Compute[" + compute_node + "]",
                "  Compute --> Storage[" + storage_node + "]",
                "  Compute --> Observability[" + availability_node + "]",
            ]
        )
