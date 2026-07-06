from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, PlainTextResponse

from app.core.config import Settings, get_settings
from app.schemas.recommendation import RecommendationResponse
from app.schemas.workload import WorkloadRequest
from app.services.recommendation_service import RecommendationService, get_recommendation_service

router = APIRouter()


@router.get("/")
def home(settings: Settings = Depends(get_settings)):
    return FileResponse(str(settings.static_dir / "index.html"))


@router.get("/health")
def health_check(settings: Settings = Depends(get_settings)):
    return {"status": "ok", "environment": settings.environment}


@router.post("/recommend", response_model=RecommendationResponse)
def recommend_architecture(
    workload: WorkloadRequest,
    service: RecommendationService = Depends(get_recommendation_service),
):
    return service.recommend(workload)


@router.post("/export")
def export_architecture(
    workload: WorkloadRequest,
    service: RecommendationService = Depends(get_recommendation_service),
    format_name: str = Query(default="mermaid", pattern="^(mermaid|terraform)$"),
):
    response = service.recommend(workload)
    export_content = service.export(response, format_name)
    return PlainTextResponse(content=export_content, media_type="text/plain")
