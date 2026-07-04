from pydantic import BaseModel
from typing import Dict, List


class Recommendation(BaseModel):
    recommendation: str
    reason: str
    tradeoffs: str
    details: Dict[str, str] = {}


class ArchitectureRecommendation(BaseModel):
    compute: Recommendation
    storage: Recommendation
    networking: Recommendation
    deployment: Recommendation
    availability: Recommendation


class CostEstimate(BaseModel):
    min_usd: int
    max_usd: int
    note: str


class AlternativeArchitecture(BaseModel):
    name: str
    description: str
    estimated_monthly_cost_usd: int
    best_for: str


class RecommendationResponse(BaseModel):
    project_name: str
    recommended_architecture: ArchitectureRecommendation
    confidence_score: float
    estimated_monthly_cost: CostEstimate
    alternatives: List[AlternativeArchitecture]
    architecture_diagram: str
