resource "azurerm_resource_group" "rg" {
  name     = "rg-carryon-carlos"
  location = "northeurope"

  tags = {
    Environment = "Production"
  }
}
