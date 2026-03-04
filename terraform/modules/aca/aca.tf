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

      env {
        name        = "OPENAI_API_KEY"
        secret_name = "openai-api-key"
      }

      env {
        name        = "KIWI_API_KEY"
        secret_name = "kiwi-api-key"
      }

      env {
        name        = "OTEL_EXPORTER_OTLP_HEADERS"
        secret_name = "otel-exporter-otlp-headers"
      }

      env {
        name        = "PHOENIX_CLIENT_HEADERS"
        secret_name = "phoenix-client-headers"
      }

      env {
        name        = "PHOENIX_COLLECTOR_ENDPOINT"
        secret_name = "phoenix-collector-endpoint"
      }
    }
  }

  secret {
    name                = "openai-api-key"
    identity            = azurerm_user_assigned_identity.aca.id
    key_vault_secret_id = "${var.key_vault_uri}secrets/OPENAI-API-KEY"
  }

  secret {
    name                = "kiwi-api-key"
    identity            = azurerm_user_assigned_identity.aca.id
    key_vault_secret_id = "${var.key_vault_uri}secrets/KIWI-API-KEY"
  }

  secret {
    name                = "otel-exporter-otlp-headers"
    identity            = azurerm_user_assigned_identity.aca.id
    key_vault_secret_id = "${var.key_vault_uri}secrets/OTEL-EXPORTER-OTLP-HEADERS"
  }

  secret {
    name                = "phoenix-client-headers"
    identity            = azurerm_user_assigned_identity.aca.id
    key_vault_secret_id = "${var.key_vault_uri}secrets/PHOENIX-CLIENT-HEADERS"
  }

  secret {
    name                = "phoenix-collector-endpoint"
    identity            = azurerm_user_assigned_identity.aca.id
    key_vault_secret_id = "${var.key_vault_uri}secrets/PHOENIX-COLLECTOR-ENDPOINT"
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.aca.id]
  }
}

resource "azurerm_user_assigned_identity" "aca" {
  name                = "${var.name}-identity"
  location            = var.location
  resource_group_name = var.resource_group_name
}
