from abc import ABC, abstractmethod

from app.providers.catalog import resolve_region, select_instance
from app.schemas.recommendation import Recommendation
from app.schemas.workload import WorkloadRequest


class ProviderAdapter(ABC):
    name: str = "generic"

    def region_for(self, workload: WorkloadRequest) -> str:
        return resolve_region(self.name, workload.region)

    def instance_for(self, workload: WorkloadRequest) -> str:
        return select_instance(self.name, workload)

    @abstractmethod
    def enrich(self, layer: str, recommendation: Recommendation, workload: WorkloadRequest) -> Recommendation:
        raise NotImplementedError
