from app.advisor.decision_engine import DecisionEngine
from app.schemas.workload import WorkloadRequest


def test_decision_engine_returns_architecture_recommendation():
    workload = WorkloadRequest(
        project_name="Test Project",
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

    engine = DecisionEngine()
    result = engine.generate(workload)

    assert result.project_name == "Test Project"
    architecture = result.recommended_architecture
    assert architecture.compute is not None
    assert architecture.storage is not None
    assert "container" in architecture.deployment.recommendation.lower()
    assert architecture.availability.details["availability_model"] == "regional"
    assert result.confidence_score >= 0.7
    assert result.estimated_monthly_cost.min_usd < result.estimated_monthly_cost.max_usd
    assert len(result.alternatives) == 3
    assert "flowchart LR" in result.architecture_diagram


def test_decision_engine_uses_high_resource_compute_rule():
    workload = WorkloadRequest(
        project_name="High Resource Project",
        cpu=12,
        ram_gb=64,
        gpu_required=False,
        storage_gb=500,
        daily_users=800,
        traffic_level="medium",
        budget="medium",
        deployment_preference="vm",
        availability="medium",
    )

    engine = DecisionEngine()
    result = engine.generate(workload)

    assert result.recommended_architecture.compute.details["compute_type"] == "compute_optimized"


def test_decision_engine_applies_provider_specific_details():
    workload = WorkloadRequest(
        project_name="Huawei Project",
        cpu=8,
        ram_gb=32,
        gpu_required=False,
        storage_gb=1000,
        daily_users=5000,
        traffic_level="high",
        budget="high",
        deployment_preference="container",
        availability="high",
        preferred_provider="huawei_cloud",
        region="eu-west-101",
    )

    engine = DecisionEngine()
    result = engine.generate(workload)

    assert result.provider == "huawei_cloud"
    assert result.region == "eu-west-101"
    assert result.recommended_architecture.compute.details["instance_type"] == "c7.2xlarge.4"
    assert "OBS" in result.recommended_architecture.storage.recommendation or "CCE" in result.recommended_architecture.deployment.recommendation
    assert result.score_breakdown.scalability >= result.score_breakdown.complexity
    assert any("availability" in note.lower() or "security" in note.lower() for note in result.validation_notes)


def test_decision_engine_supports_aws_azure_gcp_and_region_fallbacks():
    engine = DecisionEngine()

    for provider, requested_region, expected_region in [
        ("aws", "eu-central-1", "eu-central-1"),
        ("azure", "westeurope", "westeurope"),
        ("gcp", "invalid-region", "us-central1"),
    ]:
        workload = WorkloadRequest(
            project_name=f"{provider} Project",
            cpu=4,
            ram_gb=16,
            gpu_required=False,
            storage_gb=1200,
            daily_users=10000,
            traffic_level="high",
            budget="medium",
            deployment_preference="container",
            availability="high",
            preferred_provider=provider,
            region=requested_region,
        )

        result = engine.generate(workload)

        assert result.provider == provider
        assert result.region == expected_region
        assert result.recommended_architecture.compute.details["instance_type"]
        assert result.recommended_architecture.storage.details["database_service"]
        assert result.recommended_architecture.deployment.details["service_family"]


def test_decision_engine_estimates_higher_cost_for_gpu_high_availability():
    base_workload = WorkloadRequest(
        project_name="Base Project",
        cpu=2,
        ram_gb=4,
        gpu_required=False,
        storage_gb=100,
        daily_users=500,
        traffic_level="low",
        budget="low",
        deployment_preference="no_preference",
        availability="low",
    )
    demanding_workload = WorkloadRequest(
        project_name="Demanding Project",
        cpu=8,
        ram_gb=32,
        gpu_required=True,
        storage_gb=2000,
        daily_users=10000,
        traffic_level="high",
        budget="high",
        deployment_preference="container",
        availability="high",
    )

    engine = DecisionEngine()
    base = engine.generate(base_workload)
    demanding = engine.generate(demanding_workload)

    assert demanding.estimated_monthly_cost.min_usd > base.estimated_monthly_cost.max_usd
    assert "CDN" in demanding.architecture_diagram
    assert "GPU Compute" in demanding.architecture_diagram
