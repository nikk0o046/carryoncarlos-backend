provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name  = "carryon-carlos-rg"
    storage_account_name = "carryoncarlossa"
    container_name       = "tfstate"
    key                  = "terraform-base.tfstate"
  }
}

data "azurerm_client_config" "current" {}