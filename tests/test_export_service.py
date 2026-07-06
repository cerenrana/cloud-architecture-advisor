from app.schemas.recommendation import RecommendationResponse
from app.services.export_service import ExportService


def build_response() -> RecommendationResponse:
    return RecommendationResponse(
        project_name="Export Demo",
        provider="huawei_cloud",
        region="eu-west-101",
        recommended_architecture={
            "compute": {"recommendation": "x", "reason": "y", "tradeoffs": "z", "details": {"compute_type": "balanced"}},
            "storage": {"recommendation": "x", "reason": "y", "tradeoffs": "z", "details": {"storage_type": "managed_block"}},
            "networking": {"recommendation": "x", "reason": "y", "tradeoffs": "z", "details": {"network_model": "private"}},
            "deployment": {"recommendation": "x", "reason": "y", "tradeoffs": "z", "details": {"deployment_model": "container"}},
            "availability": {"recommendation": "x", "reason": "y", "tradeoffs": "z", "details": {"availability_model": "regional"}},
        },
        confidence_score=0.8,
        score_breakdown={"cost": 0.7, "scalability": 0.8, "availability": 0.7, "complexity": 0.6, "performance": 0.8},
        estimated_monthly_cost={"min_usd": 100, "max_usd": 150, "note": "n"},
        alternatives=[],
        architecture_diagram="flowchart LR",
        validation_notes=["ok"],
        security_recommendations=["IAM"],
        compliance_checks=["Compliance review"],
        disaster_recovery=["DR plan"],
        kubernetes_recommendations=["Kubernetes"],
    )


def test_export_service_builds_mermaid_and_terraform():
    service = ExportService()
    response = build_response()

    diagram = service.build_mermaid_diagram(response)
    terraform = service.build_terraform(response)

    assert "flowchart LR" in diagram
    assert "huaweicloud" in terraform.lower()
