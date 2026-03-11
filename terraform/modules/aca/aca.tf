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
        name        = "PHOENIX_COLLECTOR_ENDPOINT"
        secret_name = "phoenix-collector-endpoint"
      }

      env {
        name        = "PHOENIX_API_KEY"
        secret_name = "phoenix-api-key"
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
    name                = "phoenix-collector-endpoint"
    identity            = azurerm_user_assigned_identity.aca.id
    key_vault_secret_id = "${var.key_vault_uri}secrets/PHOENIX-COLLECTOR-ENDPOINT"
  }

  secret {
    name                = "phoenix-api-key"
    identity            = azurerm_user_assigned_identity.aca.id
    key_vault_secret_id = "${var.key_vault_uri}secrets/PHOENIX-API-KEY"
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
