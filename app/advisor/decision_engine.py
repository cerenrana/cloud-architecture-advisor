from app.providers.factory import get_provider_adapter
from app.rules.availability_rules import recommend_availability
from app.rules.compute_rules import recommend_compute
from app.rules.deployment_rules import recommend_deployment
from app.rules.network_rules import recommend_networking
from app.rules.storage_rules import recommend_storage
from app.schemas.recommendation import (
    AlternativeArchitecture,
    CostEstimate,
    RecommendationResponse,
    ScoreBreakdown,
)
from app.schemas.workload import WorkloadRequest
from app.services.enterprise_service import EnterpriseService


class DecisionEngine:
    def __init__(self, enterprise_service: EnterpriseService | None = None):
        self.enterprise_service = enterprise_service or EnterpriseService()

    def generate(self, workload: WorkloadRequest) -> RecommendationResponse:
        architecture = {
            "compute": recommend_compute(workload),
            "storage": recommend_storage(workload),
            "networking": recommend_networking(workload),
            "deployment": recommend_deployment(workload),
            "availability": recommend_availability(workload),
        }

        provider_adapter = get_provider_adapter(workload.preferred_provider)
        architecture = {
            key: provider_adapter.enrich(key, recommendation, workload)
            for key, recommendation in architecture.items()
        }

        score_breakdown = self._calculate_score_breakdown(workload, provider_adapter.name)

        return RecommendationResponse(
            project_name=workload.project_name,
            provider=provider_adapter.name,
            region=provider_adapter.region_for(workload),
            recommended_architecture=architecture,
            confidence_score=self._calculate_confidence(workload, score_breakdown),
            score_breakdown=score_breakdown,
            estimated_monthly_cost=self._estimate_cost(workload),
            alternatives=self._build_alternatives(workload),
            architecture_diagram=self._build_diagram(workload, provider_adapter.name),
            validation_notes=self._build_validation_notes(workload, provider_adapter.name),
            security_recommendations=self.enterprise_service.build_security_recommendations(workload),
            compliance_checks=self.enterprise_service.build_compliance_checks(workload),
            disaster_recovery=self.enterprise_service.build_disaster_recovery(workload),
            kubernetes_recommendations=self.enterprise_service.build_kubernetes_recommendations(workload),
        )

    def _calculate_confidence(self, workload: WorkloadRequest, score_breakdown: ScoreBreakdown) -> float:
        average_score = (
            score_breakdown.scalability
            + score_breakdown.availability
            + score_breakdown.performance
            + (1 - score_breakdown.complexity)
        ) / 4

        return round(min(0.92, max(0.65, average_score + 0.08)), 2)

    def _calculate_score_breakdown(self, workload: WorkloadRequest, provider_name: str) -> ScoreBreakdown:
        cost_score = 0.7
        scalability_score = 0.6
        availability_score = 0.55
        complexity_score = 0.45
        performance_score = 0.6

        if workload.budget == "high":
            cost_score += 0.08
        elif workload.budget == "low":
            cost_score += 0.12

        if workload.traffic_level == "high":
            scalability_score += 0.18
            performance_score += 0.12
        elif workload.traffic_level == "medium":
            scalability_score += 0.08
            performance_score += 0.07

        if workload.availability == "high":
            availability_score += 0.2
            complexity_score += 0.12
        elif workload.availability == "medium":
            availability_score += 0.1
            complexity_score += 0.06

        if workload.gpu_required:
            performance_score += 0.12
            complexity_score += 0.08

        if workload.cpu >= 8 or workload.ram_gb >= 32:
            performance_score += 0.08

        if provider_name != "generic":
            availability_score += 0.04
            scalability_score += 0.04

        return ScoreBreakdown(
            cost=round(min(0.98, cost_score), 2),
            scalability=round(min(0.98, scalability_score), 2),
            availability=round(min(0.98, availability_score), 2),
            complexity=round(min(0.95, complexity_score), 2),
            performance=round(min(0.98, performance_score), 2),
        )

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

    def _build_validation_notes(self, workload: WorkloadRequest, provider_name: str) -> list[str]:
        notes = [
            "Security validation: enforce IAM, encryption, and network segmentation.",
            "Availability validation: ensure the target deployment pattern matches the requested uptime expectation.",
        ]

        if workload.availability == "high":
            notes.append("High availability design should include multi-zone redundancy and automated recovery.")
        if workload.gpu_required:
            notes.append("GPU workloads should be validated for quota, scheduling, and storage throughput.")
        if workload.daily_users >= 5000:
            notes.append("High traffic workloads should be reviewed for autoscaling thresholds and load balancing policies.")
        if provider_name != "generic":
            notes.append(f"{provider_name} recommendations should be reviewed against regional service availability and pricing.")

        return notes

    def _build_diagram(self, workload: WorkloadRequest, provider_name: str) -> str:
        compute_node = "GPU Compute" if workload.gpu_required else "App Compute"
        storage_node = "Object Storage" if workload.storage_gb >= 1000 else "Managed Storage"
        entry_node = "CDN" if workload.traffic_level == "high" else "API Gateway"
        availability_node = "Multi-AZ Failover" if workload.availability == "high" else "Monitoring"
        provider_label = provider_name.replace("_", " ").title()

        return "\n".join(
            [
                "flowchart LR",
                "  User[Users] --> Edge[" + entry_node + "]",
                "  Edge --> LB[Load Balancer]",
                "  LB --> Compute[" + compute_node + "]",
                "  Compute --> Storage[" + storage_node + "]",
                "  Compute --> Observability[" + availability_node + "]",
                "  Compute -. Provider .-> ProviderNode[" + provider_label + "]",
            ]
        )
