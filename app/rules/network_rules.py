from app.rules.base import Rule
from app.rules.engine import evaluate_rules
from app.schemas.recommendation import Recommendation
from app.schemas.workload import WorkloadRequest


class HighTrafficNetworkingRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.traffic_level == "high"

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="Dedicated VPC with load balancing and CDN integration.",
            reason="High traffic requires a resilient network design and content delivery optimization.",
            tradeoffs="Higher networking cost and configuration complexity, but better user experience and throughput.",
            details={"network_model": "vpc", "cdn": "enabled"},
        )


class MediumTrafficNetworkingRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.traffic_level == "medium"

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="Private network with API gateway and security groups.",
            reason="Medium traffic workloads benefit from managed routing and security controls.",
            tradeoffs="Slightly more overhead than a basic network, but improves security and traffic shaping.",
            details={"network_model": "private", "gateway": "api_gateway"},
        )


def recommend_networking(workload: WorkloadRequest) -> Recommendation:
    rules = [HighTrafficNetworkingRule(), MediumTrafficNetworkingRule()]
    default = Recommendation(
        recommendation="Basic secure public network with traffic filtering.",
        reason="Lower traffic workloads can use a cost-effective network design.",
        tradeoffs="Less optimized for burst traffic but easier to operate.",
        details={"network_model": "public"},
    )
    return evaluate_rules(workload, rules, default)
