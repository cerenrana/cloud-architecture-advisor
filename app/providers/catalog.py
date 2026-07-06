from app.schemas.workload import WorkloadRequest


DEFAULT_REGIONS = {
    "aws": "us-east-1",
    "azure": "eastus",
    "gcp": "us-central1",
    "huawei_cloud": "eu-west-101",
    "generic": "global",
}

SUPPORTED_REGIONS = {
    "aws": ["us-east-1", "us-west-2", "eu-central-1", "eu-west-1"],
    "azure": ["eastus", "westus2", "westeurope", "northeurope"],
    "gcp": ["us-central1", "us-east1", "europe-west1", "europe-west4"],
    "huawei_cloud": ["eu-west-101", "ap-southeast-3", "la-south-2", "cn-north-4"],
    "generic": ["global"],
}

SERVICE_CATALOG = {
    "aws": {
        "compute": "Amazon EC2",
        "gpu_compute": "Amazon EC2 G5",
        "container_runtime": "Amazon ECS",
        "kubernetes": "Amazon EKS",
        "database": "Amazon RDS",
        "object_storage": "Amazon S3",
        "block_storage": "Amazon EBS",
        "networking": "Amazon VPC + Application Load Balancer",
        "cdn": "Amazon CloudFront",
        "availability": "Multi-AZ RDS + Auto Scaling",
    },
    "azure": {
        "compute": "Azure Virtual Machines",
        "gpu_compute": "Azure NCasT4_v3 Virtual Machines",
        "container_runtime": "Azure Container Apps",
        "kubernetes": "Azure Kubernetes Service",
        "database": "Azure Database",
        "object_storage": "Azure Blob Storage",
        "block_storage": "Azure Managed Disks",
        "networking": "Azure VNet + Application Gateway",
        "cdn": "Azure Front Door",
        "availability": "Availability Zones + VM Scale Sets",
    },
    "gcp": {
        "compute": "Compute Engine",
        "gpu_compute": "Compute Engine G2",
        "container_runtime": "Cloud Run",
        "kubernetes": "Google Kubernetes Engine",
        "database": "Cloud SQL",
        "object_storage": "Cloud Storage",
        "block_storage": "Persistent Disk",
        "networking": "VPC + Cloud Load Balancing",
        "cdn": "Cloud CDN",
        "availability": "Regional MIG + Cloud SQL HA",
    },
    "huawei_cloud": {
        "compute": "Elastic Cloud Server",
        "gpu_compute": "GPU Accelerated Cloud Server",
        "container_runtime": "Cloud Container Instance",
        "kubernetes": "Cloud Container Engine",
        "database": "Relational Database Service",
        "object_storage": "Object Storage Service",
        "block_storage": "Elastic Volume Service",
        "networking": "Virtual Private Cloud + Elastic Load Balance",
        "cdn": "Content Delivery Network",
        "availability": "Multi-AZ RDS + Auto Scaling",
    },
}

INSTANCE_CATALOG = {
    "aws": [
        {"name": "t3.small", "cpu": 2, "ram_gb": 2, "gpu": False},
        {"name": "t3.medium", "cpu": 2, "ram_gb": 4, "gpu": False},
        {"name": "m6i.large", "cpu": 2, "ram_gb": 8, "gpu": False},
        {"name": "m6i.xlarge", "cpu": 4, "ram_gb": 16, "gpu": False},
        {"name": "c6i.2xlarge", "cpu": 8, "ram_gb": 16, "gpu": False},
        {"name": "g5.xlarge", "cpu": 4, "ram_gb": 16, "gpu": True},
    ],
    "azure": [
        {"name": "Standard_B2s", "cpu": 2, "ram_gb": 4, "gpu": False},
        {"name": "Standard_D2s_v5", "cpu": 2, "ram_gb": 8, "gpu": False},
        {"name": "Standard_D4s_v5", "cpu": 4, "ram_gb": 16, "gpu": False},
        {"name": "Standard_F8s_v2", "cpu": 8, "ram_gb": 16, "gpu": False},
        {"name": "Standard_NC4as_T4_v3", "cpu": 4, "ram_gb": 28, "gpu": True},
    ],
    "gcp": [
        {"name": "e2-small", "cpu": 2, "ram_gb": 2, "gpu": False},
        {"name": "e2-standard-2", "cpu": 2, "ram_gb": 8, "gpu": False},
        {"name": "e2-standard-4", "cpu": 4, "ram_gb": 16, "gpu": False},
        {"name": "c3-standard-8", "cpu": 8, "ram_gb": 32, "gpu": False},
        {"name": "g2-standard-4", "cpu": 4, "ram_gb": 16, "gpu": True},
    ],
    "huawei_cloud": [
        {"name": "s6.large.2", "cpu": 2, "ram_gb": 4, "gpu": False},
        {"name": "s6.xlarge.2", "cpu": 4, "ram_gb": 8, "gpu": False},
        {"name": "c7.2xlarge.4", "cpu": 8, "ram_gb": 32, "gpu": False},
        {"name": "pi2.2xlarge.4", "cpu": 8, "ram_gb": 32, "gpu": True},
    ],
}


def resolve_region(provider: str, requested_region: str | None) -> str:
    supported = SUPPORTED_REGIONS.get(provider, SUPPORTED_REGIONS["generic"])
    if requested_region in supported:
        return requested_region
    return DEFAULT_REGIONS.get(provider, DEFAULT_REGIONS["generic"])


def select_instance(provider: str, workload: WorkloadRequest) -> str:
    candidates = INSTANCE_CATALOG.get(provider, [])
    matching_gpu = [item for item in candidates if item["gpu"] is workload.gpu_required]
    pool = matching_gpu or candidates

    for item in pool:
        if item["cpu"] >= workload.cpu and item["ram_gb"] >= workload.ram_gb:
            return str(item["name"])

    if pool:
        return str(pool[-1]["name"])

    return "custom"


def provider_services(provider: str) -> dict[str, str]:
    return SERVICE_CATALOG.get(provider, {})
