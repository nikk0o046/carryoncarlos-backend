resource "azurerm_container_app_environment" "aca_environment" {
  name                       = var.name
  location                   = var.location
  resource_group_name        = var.resource_group_name
  logs_destination           = var.logs_destination
  log_analytics_workspace_id = var.log_analytics_workspace_id
}
