from app.providers.base import ProviderAdapter
from app.providers.aws import AwsProviderAdapter
from app.providers.azure import AzureProviderAdapter
from app.providers.huawei import HuaweiProviderAdapter
from app.providers.gcp import GcpProviderAdapter


class GenericProviderAdapter(ProviderAdapter):
    name = "generic"

    def enrich(self, layer: str, recommendation, workload):
        recommendation = recommendation.model_copy(deep=True)
        details = dict(recommendation.details)
        details.setdefault("provider", self.name)
        details["region"] = self.region_for(workload)
        recommendation.details = details
        return recommendation


def get_provider_adapter(preferred_provider: str | None) -> ProviderAdapter:
    adapters = {
        "huawei_cloud": HuaweiProviderAdapter(),
        "aws": AwsProviderAdapter(),
        "azure": AzureProviderAdapter(),
        "gcp": GcpProviderAdapter(),
    }
    return adapters.get(preferred_provider or "generic", GenericProviderAdapter())
