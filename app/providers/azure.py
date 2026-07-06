from app.providers.base import ProviderAdapter
from app.providers.catalog import provider_services
from app.schemas.recommendation import Recommendation
from app.schemas.workload import WorkloadRequest


class AzureProviderAdapter(ProviderAdapter):
    name = "azure"

    def enrich(self, layer: str, recommendation: Recommendation, workload: WorkloadRequest) -> Recommendation:
        details = dict(recommendation.details)
        services = provider_services(self.name)
        details.setdefault("provider", self.name)
        details["region"] = self.region_for(workload)

        if layer == "compute":
            details["service_family"] = services["gpu_compute"] if workload.gpu_required else services["compute"]
            details["instance_type"] = self.instance_for(workload)
        elif layer == "storage":
            details["service_family"] = services["object_storage"] if workload.storage_gb >= 1000 else services["block_storage"]
            details["database_service"] = services["database"]
        elif layer == "networking":
            details["service_family"] = services["cdn"] if workload.traffic_level == "high" else services["networking"]
        elif layer == "deployment":
            details["service_family"] = services["kubernetes"] if workload.deployment_preference == "container" else services["container_runtime"]
        elif layer == "availability":
            details["service_family"] = services["availability"]

        recommendation = recommendation.model_copy(deep=True)
        recommendation.details = details
        return recommendation
