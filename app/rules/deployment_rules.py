from app.rules.base import Rule
from app.rules.engine import evaluate_rules
from app.schemas.recommendation import Recommendation
from app.schemas.workload import WorkloadRequest


class ContainerDeploymentRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.deployment_preference == "container"

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="Managed container orchestration platform (Kubernetes or CCE).",
            reason="The preference is for containers, so a container service provides portability and scalability.",
            tradeoffs="Requires container expertise and orchestration setup, but improves deployment agility.",
            details={"deployment_model": "container_orchestration"},
        )


class VmDeploymentRule(Rule):
    def applies_to(self, workload: WorkloadRequest) -> bool:
        return workload.deployment_preference == "vm"

    def recommend(self, workload: WorkloadRequest) -> Recommendation:
        return Recommendation(
            recommendation="Virtual machines with managed instance groups.",
            reason="A VM-based deployment is appropriate when the workload depends on traditional VM environments.",
            tradeoffs="Less flexible than containers, but simpler for legacy applications.",
            details={"deployment_model": "vm"},
        )


def recommend_deployment(workload: WorkloadRequest) -> Recommendation:
    rules = [ContainerDeploymentRule(), VmDeploymentRule()]
    default = Recommendation(
        recommendation="Serverless or container-ready deployment with minimal operational overhead.",
        reason="No strong deployment preference allows us to choose an efficient managed platform.",
        tradeoffs="May not fit workloads requiring dedicated VM-level control.",
        details={"deployment_model": "managed_service"},
    )
    return evaluate_rules(workload, rules, default)
