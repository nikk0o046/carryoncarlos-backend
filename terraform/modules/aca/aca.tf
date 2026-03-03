resource "azurerm_container_app" "aca" {
  name                         = var.name
  container_app_environment_id = var.container_app_environment_id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  ingress {
    external_enabled = true
    target_port      = 8080
    traffic_weight {
      percentage = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 0
    max_replicas = 2

    container {
      name   = var.name
      image  = "ghcr.io/nikk0o046/carryoncarlos-backend:${var.image_tag}"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }
}
