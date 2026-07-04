from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI(
    title="Cloud Architecture Advisor",
    description="A rule-based cloud architecture recommendation API.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)
