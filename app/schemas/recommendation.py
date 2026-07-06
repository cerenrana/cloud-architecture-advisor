from pydantic import BaseModel, Field
from typing import Dict, List


class Recommendation(BaseModel):
    recommendation: str
    reason: str
    tradeoffs: str
    details: Dict[str, str] = Field(default_factory=dict)


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


class ScoreBreakdown(BaseModel):
    cost: float
    scalability: float
    availability: float
    complexity: float
    performance: float


class AlternativeArchitecture(BaseModel):
    name: str
    description: str
    estimated_monthly_cost_usd: int
    best_for: str


class RecommendationResponse(BaseModel):
    project_name: str
    provider: str
    region: str
    recommended_architecture: ArchitectureRecommendation
    confidence_score: float
    score_breakdown: ScoreBreakdown
    estimated_monthly_cost: CostEstimate
    alternatives: List[AlternativeArchitecture]
    architecture_diagram: str
    validation_notes: List[str]
    security_recommendations: List[str]
    compliance_checks: List[str]
    disaster_recovery: List[str]
    kubernetes_recommendations: List[str]
