# Cloud Architecture Advisor

Cloud Architecture Advisor is a FastAPI-based decision-support platform that analyzes workload requirements and recommends an appropriate cloud architecture. It combines rule-based reasoning with provider-aware guidance for AWS, Azure, Google Cloud, Huawei Cloud, and generic deployments.

## What it does

- Evaluates workload characteristics such as CPU, memory, storage, traffic, budget, and availability
- Recommends compute, storage, networking, deployment, and availability strategies
- Selects provider regions and realistic instance families for AWS, Azure, Google Cloud, and Huawei Cloud
- Adds provider service names such as Amazon EKS/ECS/RDS/S3, Azure AKS/Blob Storage, GKE/Cloud SQL, and Huawei CCE/RDS/OBS
- Produces enterprise-oriented guidance for security, compliance, disaster recovery, and Kubernetes
- Supports export to Mermaid and Terraform-style architecture artifacts

## Architecture at a glance

The service is organized into a clean layered structure:

- API layer: FastAPI routes and request handling
- Domain layer: recommendation rules and decision logic
- Service layer: orchestration and export operations
- Provider layer: vendor-specific enrichment and recommendations

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000.

## API endpoints

- GET /health — health check
- POST /recommend — generate a recommendation from workload input
- POST /export?format_name=mermaid|terraform — export the latest recommendation as text

## Example request

```bash
curl -X POST http://127.0.0.1:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Retail Analytics",
    "cpu": 8,
    "ram_gb": 16,
    "gpu_required": false,
    "storage_gb": 500,
    "daily_users": 20000,
    "traffic_level": "high",
    "budget": "medium",
    "deployment_preference": "container",
    "availability": "high",
    "preferred_provider": "aws",
    "region": "eu-central-1"
  }'
```

## Example export

```bash
curl -X POST "http://127.0.0.1:8000/export?format_name=terraform" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Retail Analytics",
    "cpu": 8,
    "ram_gb": 16,
    "gpu_required": false,
    "storage_gb": 500,
    "daily_users": 20000,
    "traffic_level": "high",
    "budget": "medium",
    "deployment_preference": "container",
    "availability": "high",
    "preferred_provider": "aws",
    "region": "eu-central-1"
  }'
```

## Roadmap

- V2: Multi-provider support, region selection, realistic instance selection, and provider service names
- V3: Live AWS pricing, richer Terraform output, and Kubernetes YAML generation
- V4: OpenAI-powered architecture explanations, cost optimization, scaling simulations, and migration guidance
- V5: PostgreSQL-backed saved projects, Redis caching, and Kubernetes deployment packaging

## Running tests

```bash
pytest -q
```

## Container and CI support

A Dockerfile and a GitHub Actions workflow are included for packaging and automated test execution.

```bash
docker build -t cloud-architecture-advisor .
docker run -p 8000:8000 cloud-architecture-advisor
```
