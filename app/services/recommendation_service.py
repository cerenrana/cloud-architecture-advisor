import logging
from typing import Optional

from app.advisor.decision_engine import DecisionEngine
from app.core.config import Settings, get_settings
from app.services.export_service import ExportService


class RecommendationService:
    def __init__(self, decision_engine: Optional[DecisionEngine] = None, settings: Optional[Settings] = None, export_service: Optional[ExportService] = None):
        self.decision_engine = decision_engine or DecisionEngine()
        self.settings = settings or get_settings()
        self.export_service = export_service or ExportService()
        self.logger = logging.getLogger(__name__)

    def recommend(self, workload):
        self.logger.info("Generating recommendation for %s", workload.project_name)
        return self.decision_engine.generate(workload)

    def export(self, response, format_name: str) -> str:
        if format_name == "terraform":
            return self.export_service.build_terraform(response)
        return self.export_service.build_mermaid_diagram(response)


def get_recommendation_service() -> RecommendationService:
    return RecommendationService()
