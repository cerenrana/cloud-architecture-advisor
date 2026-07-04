from abc import ABC, abstractmethod
from app.schemas.workload import WorkloadRequest


class Rule(ABC):
    @abstractmethod
    def applies_to(self, workload: WorkloadRequest) -> bool:
        pass

    @abstractmethod
    def recommend(self, workload):
        pass
