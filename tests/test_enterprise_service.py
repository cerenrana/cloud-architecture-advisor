from app.schemas.workload import WorkloadRequest
from app.services.enterprise_service import EnterpriseService


def test_enterprise_service_generates_security_and_dr_guidance():
    service = EnterpriseService()
    workload = WorkloadRequest(
        project_name="Enterprise Test",
        cpu=8,
        ram_gb=32,
        gpu_required=True,
        storage_gb=2000,
        daily_users=10000,
        traffic_level="high",
        budget="high",
        deployment_preference="container",
        availability="high",
        preferred_provider="huawei_cloud",
    )

    security = service.build_security_recommendations(workload)
    compliance = service.build_compliance_checks(workload)
    dr = service.build_disaster_recovery(workload)
    k8s = service.build_kubernetes_recommendations(workload)

    assert any("IAM" in item for item in security)
    assert any("compliance" in item.lower() for item in compliance)
    assert any("failover" in item.lower() for item in dr)
    assert any("Kubernetes" in item for item in k8s)
