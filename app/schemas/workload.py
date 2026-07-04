from pydantic import BaseModel, Field
from typing import Literal


class WorkloadRequest(BaseModel):
    project_name: str = Field(..., description="Project name")

    cpu: int = Field(..., ge=1)
    ram_gb: int = Field(..., ge=1)

    gpu_required: bool

    storage_gb: int = Field(..., ge=1)

    daily_users: int = Field(..., ge=1)

    traffic_level: Literal[
        "low",
        "medium",
        "high"
    ]

    budget: Literal[
        "low",
        "medium",
        "high"
    ]

    deployment_preference: Literal[
        "vm",
        "container",
        "no_preference"
    ]

    availability: Literal[
        "low",
        "medium",
        "high"
    ]