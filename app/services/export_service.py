from pathlib import Path

from app.schemas.recommendation import RecommendationResponse


class ExportService:
    def build_mermaid_diagram(self, response: RecommendationResponse) -> str:
        return response.architecture_diagram

    def build_terraform(self, response: RecommendationResponse) -> str:
        provider = response.provider
        if provider == "huawei_cloud":
            return self._build_huawei_terraform(response)
        if provider == "aws":
            return self._build_aws_terraform(response)
        if provider == "azure":
            return self._build_azure_terraform(response)
        if provider == "gcp":
            return self._build_gcp_terraform(response)
        return self._build_generic_terraform(response)

    def _build_huawei_terraform(self, response: RecommendationResponse) -> str:
        return "\n".join(
            [
                "terraform {",
                "  required_providers {",
                "    huaweicloud = { source = \"huaweicloud/huaweicloud\" }",
                "  }",
                "}",
                "",
                f"provider \"huaweicloud\" {{ region = \"{response.region}\" }}",
                "",
                "resource \"huaweicloud_compute_instance\" \"app\" {",
                f"  name              = \"{response.project_name.lower().replace(' ', '-')}-app\"",
                "  image_name        = \"Ubuntu 22.04\"",
                f"  flavor_name       = \"{response.recommended_architecture.compute.details.get('instance_type', 's6.large.2')}\"",
                "  availability_zone = \"az1\"",
                "}",
            ]
        )

    def _build_aws_terraform(self, response: RecommendationResponse) -> str:
        return "\n".join(
            [
                "terraform {",
                "  required_providers {",
                "    aws = { source = \"hashicorp/aws\" }",
                "  }",
                "}",
                "",
                f"provider \"aws\" {{ region = \"{response.region}\" }}",
                "",
                "resource \"aws_instance\" \"app\" {",
                "  ami           = \"ami-0c02fb55956c6d318\"",
                f"  instance_type = \"{response.recommended_architecture.compute.details.get('instance_type', 't3.medium')}\"",
                "}",
            ]
        )

    def _build_azure_terraform(self, response: RecommendationResponse) -> str:
        return "\n".join(
            [
                "terraform {",
                "  required_providers {",
                "    azurerm = { source = \"hashicorp/azurerm\" }",
                "  }",
                "}",
                "",
                "provider \"azurerm\" { features {} }",
                "",
                "resource \"azurerm_linux_virtual_machine\" \"app\" {",
                f"  name                = \"{response.project_name.lower().replace(' ', '-')}-app\"",
                "  resource_group_name = \"rg-demo\"",
                f"  location            = \"{response.region}\"",
                f"  size                = \"{response.recommended_architecture.compute.details.get('instance_type', 'Standard_B2s')}\"",
                "}",
            ]
        )

    def _build_gcp_terraform(self, response: RecommendationResponse) -> str:
        return "\n".join(
            [
                "terraform {",
                "  required_providers {",
                "    google = { source = \"hashicorp/google\" }",
                "  }",
                "}",
                "",
                f"provider \"google\" {{ region = \"{response.region}\" }}",
                "",
                "resource \"google_compute_instance\" \"app\" {",
                f"  name         = \"{response.project_name.lower().replace(' ', '-')}-app\"",
                f"  machine_type = \"{response.recommended_architecture.compute.details.get('instance_type', 'e2-standard-2')}\"",
                "  zone         = \"us-central1-a\"",
                "  boot_disk { initialize_params { image = \"debian-cloud/debian-12\" } }",
                "  network_interface { network = \"default\" }",
                "}",
            ]
        )

    def _build_generic_terraform(self, response: RecommendationResponse) -> str:
        return "# Generic placeholder Terraform export"
