resource "azurerm_key_vault" "keyvault" {
  name                        = "${var.name}-kv"
  location                    = var.location
  resource_group_name         = var.resource_group_name
  tenant_id                   = var.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false
  sku_name = "standard"

  access_policy {
    tenant_id = var.tenant_id
    object_id = var.principal_id

    secret_permissions = [
      "Get",
      "List"
    ]
  }
}
