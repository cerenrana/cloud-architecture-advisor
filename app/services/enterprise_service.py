from app.schemas.workload import WorkloadRequest


class EnterpriseService:
    def build_security_recommendations(self, workload: WorkloadRequest) -> list[str]:
        recommendations = [
            "Enable IAM least-privilege access and role-based access control.",
            "Encrypt data at rest and in transit using managed keys or customer-managed keys.",
            "Segment the network with private subnets, security groups, and firewall policies.",
        ]
        if workload.gpu_required:
            recommendations.append("Protect GPU workloads with separate network policies and access controls.")
        return recommendations

    def build_compliance_checks(self, workload: WorkloadRequest) -> list[str]:
        checks = [
            "Review data residency and regional compliance requirements.",
            "Ensure backup and retention policies align with internal controls.",
        ]
        if workload.daily_users >= 5000:
            checks.append("Validate audit logging coverage for high-throughput environments.")
        return checks

    def build_disaster_recovery(self, workload: WorkloadRequest) -> list[str]:
        recommendations = [
            "Define RPO/RTO targets and align backup strategy to business criticality.",
            "Use multi-zone or multi-region replication where availability requirements justify it.",
        ]
        if workload.availability == "high":
            recommendations.append("Implement automated failover and regional DR rehearsal procedures.")
        return recommendations

    def build_kubernetes_recommendations(self, workload: WorkloadRequest) -> list[str]:
        recommendations = ["Use managed Kubernetes for containerized workloads with autoscaling enabled."]
        if workload.daily_users >= 5000:
            recommendations.append("Adopt cluster autoscaling, pod disruption budgets, and service mesh policies.")
        if workload.gpu_required:
            recommendations.append("Provision GPU node pools and dedicated scheduling taints/tolerations.")
        return recommendations
