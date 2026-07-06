from app.schemas.workload import WorkloadRequest
from app.services.recommendation_service import RecommendationService


def test_recommendation_service_returns_recommendation_response():
    service = RecommendationService()
    workload = WorkloadRequest(
        project_name="Service Test",
        cpu=4,
        ram_gb=16,
        gpu_required=False,
        storage_gb=250,
        daily_users=200,
        traffic_level="medium",
        budget="medium",
        deployment_preference="container",
        availability="medium",
    )

    response = service.recommend(workload)

    assert response.project_name == "Service Test"
    assert response.confidence_score > 0
    assert response.estimated_monthly_cost.min_usd > 0
    assert len(response.alternatives) == 3
