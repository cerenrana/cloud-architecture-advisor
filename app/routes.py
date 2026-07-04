from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.advisor.decision_engine import DecisionEngine
from app.schemas.workload import WorkloadRequest
from app.schemas.recommendation import RecommendationResponse

router = APIRouter()


@router.get("/")
def home():
    return FileResponse("app/static/index.html")


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/recommend", response_model=RecommendationResponse)
def recommend_architecture(workload: WorkloadRequest):
    engine = DecisionEngine()
    return engine.generate(workload)
