import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    app_name: str = "Cloud Architecture Advisor"
    environment: str = "development"
    log_level: str = "INFO"
    static_dir: Path = PROJECT_ROOT / "app" / "static"
    project_root: Path = PROJECT_ROOT


def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Cloud Architecture Advisor"),
        environment=os.getenv("APP_ENV", "development"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        static_dir=Path(os.getenv("STATIC_DIR", str(PROJECT_ROOT / "app" / "static"))),
        project_root=PROJECT_ROOT,
    )
