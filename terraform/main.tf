resource "azurerm_resource_group" "rg" {
  name     = "${var.app_name}-rg"
  location = var.location
}

module "loganalytics" {
  source                       = "./modules/log-analytics"
  log_analytics_workspace_name = "${var.app_name}la"
  location                     = var.location
  log_analytics_workspace_sku  = "PerGB2018"
  resource_group_name          = azurerm_resource_group.rg.name
}

module "appinsights" {
  source              = "./modules/appinsights"
  name                = "${var.app_name}insights"
  location            = var.location
  application_type    = "web"
  resource_group_name = azurerm_resource_group.rg.name
}

module "aca-environment" {
  source                     = "./modules/aca-environment"
  name                       = "${var.app_name}aca-environment"
  location                   = var.location
  resource_group_name        = azurerm_resource_group.rg.name
  logs_destination           = "log-analytics"
  log_analytics_workspace_id = module.loganalytics.workspace_id
}

module "aca" {
  source                       = "./modules/aca"
  name                         = "${var.app_name}aca"
  location                     = var.location
  resource_group_name          = azurerm_resource_group.rg.name
  container_app_environment_id = module.aca-environment.id
  image_tag                    = var.image_tag
}

module "keyvault" {
  source              = "./modules/keyvault"
  name                = "${var.app_name}kv"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  principal_id        = module.aca.principal_id
  tenant_id           = data.azurerm_client_config.current.tenant_id
}
